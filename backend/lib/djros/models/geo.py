from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from geoposition.fields import GeopositionField
from .capsman import Cap, RemoteCap


class CapCoords(models.Model):
    """
    Geolocation coordinates of Client AP (CAP, ie., either InterfaceCap or RemoteCap).
    
    """
    name = models.CharField(max_length=100)
    coords = GeopositionField()

    # limit = models.Q(app_label='djros', model='Cap') | \
    #     models.Q(app_label='djros', model='RemoteCap')
    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_('Associated Cap (eg. Cap, RemoteCap)'),
        # limit_choices_to=limit,
        null=True,
        blank=True,
    )
    object_id = models.PositiveIntegerField(
        verbose_name=_('related object'),
        null=True,
    )
    cap = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return self.name
