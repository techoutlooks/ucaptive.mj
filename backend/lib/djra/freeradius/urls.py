from django.conf.urls import url, include
from rest_framework import routers
from . import api


# Freeradius v3.0 API

router = routers.SimpleRouter()
router.register(r'radusers', api.RadUserApi, base_name='raduser')
router.register(r'radgroups', api.RadGroupApi, base_name='radgroup')

urlpatterns = [
    url(r'^', include(router.urls, namespace='api')),
]