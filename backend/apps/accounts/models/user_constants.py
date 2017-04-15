
# todo: move all to django-constance

from enum import Enum
from django.utils.translation import ugettext_lazy as _


# number of credits before they get special features
# such as adding extra users
PRO_CREDITS_THRESHOLD = 100000

FREE_PLAN = 'FREE'
TRIAL_PLAN = 'TRIAL'
TIER1_PLAN = 'TIER1'
TIER2_PLAN = 'TIER2'
TIER3_PLAN = 'TIER3'

TIER_39_PLAN = 'TIER_39'
TIER_249_PLAN = 'TIER_249'
TIER_449_PLAN = 'TIER_449'

DAYFIRST = 'D'
MONTHFIRST = 'M'

PLANS = ((FREE_PLAN, _("Free Plan")),
         (TRIAL_PLAN, _("Trial")),
         (TIER_39_PLAN, _("Bronze")),
         (TIER1_PLAN, _("Silver")),
         (TIER2_PLAN, _("Gold (Legacy)")),
         (TIER3_PLAN, _("Platinum (Legacy)")),
         (TIER_249_PLAN, _("Gold")),
         (TIER_449_PLAN, _("Platinum")))

# cache keys and TTLs
USER_LOCK_KEY = 'org:%d:lock:%s'
USER_CREDITS_TOTAL_CACHE_KEY = 'org:%d:cache:credits_total'
USER_CREDITS_PURCHASED_CACHE_KEY = 'org:%d:cache:credits_purchased'
USER_CREDITS_USED_CACHE_KEY = 'org:%d:cache:credits_used'
USER_ACTIVE_TOPUP_KEY = 'org:%d:cache:active_topup'
USER_ACTIVE_TOPUP_REMAINING = 'org:%d:cache:credits_remaining:%d'
USER_CREDIT_EXPIRING_CACHE_KEY = 'org:%d:cache:credits_expiring_soon'
USER_LOW_CREDIT_THRESHOLD_CACHE_KEY = 'org:%d:cache:low_credits_threshold'

USER_LOCK_TTL = 60  # 1 minute
USER_CREDITS_CACHE_TTL = 7 * 24 * 60 * 60  # 1 week


class UserEvent(Enum):
    """
    Represents an internal user event
    """
    topup_new = 16
    topup_updated = 17


class UserCache(Enum):
    """
    User-level cache types
    """
    display = 1
    credits = 2