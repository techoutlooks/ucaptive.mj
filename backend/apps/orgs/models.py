import os
from django.db import models
from rest_framework_api_key.models import AbstractAPIKey

from contacts.models import Company, Person


class Org(Company):
    """ 
    An organization that owns features available in apps.* 
    
    """

    # some more fields
    # admin_contact = models.ForeignKey
    # technical_contact = Person()
    is_active = models.BooleanField(default=True, help_text="Whether enabled or not.")


# class Employee(Person):
#     pass


class OrgApiKeyToken(AbstractAPIKey):
    org = models.ForeignKey(Org)
    is_active = models.BooleanField(default=True)