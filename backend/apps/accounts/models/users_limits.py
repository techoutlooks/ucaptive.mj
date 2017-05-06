# -*- coding: utf-8 -*-
"""
User limits
"""
from __future__ import unicode_literals

from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.db import models, connection
from django.db.models import Sum
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django_redis import get_redis_connection

from lib.mixins import get_cacheable_result, incrby_existing
from .user_constants import *


@python_2_unicode_compatible
class Plan(models.Model):
    """
    User credits, limits, and authorizations.

    """
    name = models.CharField(verbose_name=_("Plan"), max_length=16, choices=PLANS, default=TRIAL_PLAN,
                            help_text=_("What plan the user is on"))
    start = models.DateTimeField(verbose_name=_("Plan Start"), auto_now_add=True,
                                      help_text=_("When the user switched to this plan"))
    timezone = models.CharField(verbose_name=_("Timezone"), max_length=64)
    slug = models.SlugField(verbose_name=_("Slug"), max_length=255, null=True, blank=True, unique=True,
                            error_messages=dict(unique=_("This slug is not available")))

    def __str__(self):
        pass

    @classmethod
    def get_unique_slug(cls, name):
        slug = slugify(name)

        unique_slug = slug
        if unique_slug:
            existing = cls.objects.filter(slug=unique_slug).exists()
            count = 2
            while existing:
                unique_slug = "%s-%d" % (slug, count)
                existing = cls.objects.filter(slug=unique_slug).exists()
                count += 1

            return unique_slug

    def is_free_plan(self):
        return self.name == FREE_PLAN or self.name == TRIAL_PLAN

    def get_credits_total(self, force_dirty=False):
        """
        Gets the total number of credits purchased or assigned to this user
        """
        return get_cacheable_result(USER_CREDITS_TOTAL_CACHE_KEY % self.pk, USER_CREDITS_CACHE_TTL,
                                    self._calculate_credits_total, force_dirty=force_dirty)

    def _calculate_credits_total(self):
        active_credits = self.topups.filter(is_active=True, expires_on__gte=timezone.now()).aggregate(Sum('credits')).get('credits__sum')
        active_credits = active_credits if active_credits else 0

        # these are the credits that have been used in expired topups
        expired_credits = TopUpCredits.objects.filter(
            topup__org=self, topup__is_active=True, topup__expires_on__lte=timezone.now()
        ).aggregate(Sum('used')).get('used__sum')

        expired_credits = expired_credits if expired_credits else 0

        return active_credits + expired_credits

    def get_credits_used(self):
        """
        Gets the number of credits used by this orgs
        """
        return get_cacheable_result(USER_CREDITS_USED_CACHE_KEY % self.pk, USER_CREDITS_CACHE_TTL,
                                    self._calculate_credits_used)

    def _calculate_credits_used(self):
        used_credits_sum = TopUpCredits.objects.filter(topup__org=self, topup__is_active=True)
        used_credits_sum = used_credits_sum.aggregate(Sum('used')).get('used__sum')
        used_credits_sum = used_credits_sum if used_credits_sum else 0

        unassigned_sum = self.msgs.filter(contact__is_test=False, topup=None, purged=False).count()

        return used_credits_sum + unassigned_sum

    def get_credits_remaining(self):
        """
        Gets the number of credits remaining for this orgs
        """
        return self.get_credits_total() - self.get_credits_used()

    def decrement_credit(self):
        """
        Decrements this orgs credit by 1. Returns the id of the active topup which can then be assigned to the message
        or IVR action which is being paid for with this credit
        """
        total_used_key = USER_CREDITS_USED_CACHE_KEY % self.pk
        incrby_existing(total_used_key, 1)

        active_topup = self._calculate_active_topup()
        return active_topup.pk if active_topup else None


class TopUp(models.Model):
    """
    TopUps are used to track usage across the platform. Each TopUp represents a certain number of
    credits that can be consumed by products.

    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='topups',
                            help_text="The organization that was toppped up")
    price = models.IntegerField(verbose_name=_("Price Paid"),
                                help_text=_("The price paid for the products in this top up (in cents)"))
    credits = models.IntegerField(verbose_name=_("Number of Credits"),
                                  help_text=_("The number of credits bought in this top up"))
    expires_on = models.DateTimeField(verbose_name=_("Expiration Date"),
                                      help_text=_("The date that this top up will expire"))
    stripe_charge = models.CharField(verbose_name=_("Stripe Charge Id"), max_length=32, null=True, blank=True,
                                     help_text=_("The Stripe charge id for this charge"))
    comment = models.CharField(max_length=255, null=True, blank=True,
                               help_text="Any comment associated with this topup, used when we credit one_accounts")

    @classmethod
    def create(cls, user, price, credits, stripe_charge=None, org=None):
        """
        Creates a new topup
        """
        expires_on = timezone.now() + timedelta(days=365)  # credits last 1 year

        topup = TopUp.objects.create(user=user, price=price, credits=credits, expires_on=expires_on,
                                     stripe_charge=stripe_charge, created_by=user, modified_by=user)

        user.update_caches(UserEvent.topup_new, topup)
        return topup

    def dollars(self):
        if self.price == 0:
            return 0
        else:
            return Decimal(self.price) / Decimal(100)

    def revert_topup(self):
        # unwind any items that were assigned to this topup
        self.msgs.update(topup=None)

        # mark this topup as inactive
        self.is_active = False
        self.save()

    # def get_stripe_charge(self):
    #     try:
    #         stripe.api_key = get_stripe_credentials()[1]
    #         return stripe.Charge.retrieve(self.stripe_charge)
    #     except Exception:
    #         traceback.print_exc()
    #         return None

    def get_used(self):
        """
        Calculates how many topups have actually been used
        """
        used = TopUpCredits.objects.filter(topup=self).aggregate(used=Sum('used'))
        return 0 if not used['used'] else used['used']

    def get_remaining(self):
        """
        Returns how many credits remain on this topup
        """
        return self.credits - self.get_used()

    def __unicode__(self):
        return "%s Credits" % self.credits


class TopUpCredits(models.Model):
    """
    Used to track number of credits used on a topup, mostly maintained by triggers on Msg insertion.

    """
    topup = models.ForeignKey(TopUp,
                              help_text=_("The topup these credits are being used against"))
    used = models.IntegerField(help_text=_("How many credits were used, can be negative"))

    LAST_SQUASH_KEY = 'last_topupcredits_squash'

    @classmethod
    def squash_credits(cls):
        # get the id of the last count we squashed
        r = get_redis_connection()
        last_squash = r.get(TopUpCredits.LAST_SQUASH_KEY)
        if not last_squash:
            last_squash = 0

        # get the unique flow ids for all new ones
        start = time.time()
        squash_count = 0
        for credits in TopUpCredits.objects.filter(id__gt=last_squash).order_by('topup_id').distinct('topup_id'):
            print "Squashing: %d" % credits.topup_id

            # perform our atomic squash in SQL by calling our squash method
            with connection.cursor() as c:
                c.execute("SELECT temba_squash_topupcredits(%s);", (credits.topup_id,))

            squash_count += 1

        # insert our new top squashed id
        max_id = TopUpCredits.objects.all().order_by('-id').first()
        if max_id:
            r.set(TopUpCredits.LAST_SQUASH_KEY, max_id.id)

        print "Squashed topupcredits for %d pairs in %0.3fs" % (squash_count, time.time() - start)
