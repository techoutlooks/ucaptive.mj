# -*- coding: utf-8 -*-
from __future__ import unicode_literals
__author__ = "ceduth"


"""
Custom form to register a U-Reporter.

"""
import json
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from registration.forms import RegistrationForm
from lib.utils.fields.forms import EmptyChoiceField


# styling
from djng.styling.bootstrap3.forms import Bootstrap3Form
from djng.forms import NgFormValidationMixin, NgModelFormMixin
from djng.styling.bootstrap3.forms import Bootstrap3ModelForm
from lib.utils.widgets.ng_dal_select2 import NgModelSelect2, NgSelect
from dal import autocomplete

from ..models import Reporter, Profile
from apps.cities.models import Region, City
from ..constants import (
    PHONE_NUMBER_REGEX, PHONE_NUMBER_ERROR_MSG,
    GENDER_CHOICES)


def validate_password(value):
    if not len(value) > 5:
        raise ValidationError('+6 alphanumeric characters !')


class NgLoginForm(NgModelFormMixin, NgFormValidationMixin, Bootstrap3Form, AuthenticationForm):
    """
    Angular Login Form with real-time client-side validation. Same validation occurs a second time,
    when the server receives the form's data for final processing without sacrificing to DRY.

    Browsers internal Form validation must be disabled. This is achieved by adding the property
    novalidate to the Form's HTML element.

    """

    username = forms.RegexField(PHONE_NUMBER_REGEX, required=True, label='',
                                widget=forms.TextInput(attrs={'placeholder': _('Mobile Number')}),
                                error_messages={'invalid': PHONE_NUMBER_ERROR_MSG})
    password = forms.CharField(required=True, label='',
                               widget=forms.PasswordInput(attrs={'placeholder': _('Password')}),
                               validators=[validate_password])

    # help_text=_('Your password should contain more than 6 alphanumeric characters !'))

    class Meta:
        fields = ('username', 'password',)


class NgUserForm(NgModelFormMixin, NgFormValidationMixin, Bootstrap3ModelForm):
    """
    Angular model User form which enforces uniqueness of phone number.

    """
    username = forms.RegexField(PHONE_NUMBER_REGEX, required=True, label='',
                                widget=forms.TextInput(attrs={'placeholder': _('Mobile Number')}),
                                error_messages={'invalid': PHONE_NUMBER_ERROR_MSG})
    password = forms.CharField(required=True, label='',
                               widget=forms.PasswordInput(attrs={'placeholder': _('Password')}),
                               validators=[validate_password])
    email = forms.EmailField(label='', required=False, widget=forms.TextInput(attrs={'type': 'email', 'placeholder': _('Email')}))
    first_name = forms.CharField(required=True, label='', widget=forms.TextInput(attrs={'placeholder': _('First Name')}))
    last_name = forms.CharField(required=True, label='', widget=forms.TextInput(attrs={'placeholder': _('Last Name')}))
    time_spent = forms.TimeField(label=_("Total connection time"),)

    class Meta:
        model = Reporter
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(NgUserForm, self).__init__(*args, **kwargs)

        # show time spent only to admins and inside reporter profile
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields.update({
                'time_spent': forms.CharField(widget=forms.TimeField()),
            })
            self.fields['time_spent'].widget.attrs['readonly'] = True
        else:
            self.fields.pop('time_spent')

    def clean_mobile_number(self):
        """
        Validate that the supplied email address is unique for the
        site.

        """
        if Reporter.objects.filter(mobile_number__iexact=self.cleaned_data['mobile_number']):
            raise forms.ValidationError(_("This mobile phone is already in use. Please supply a different one."))
        return self.cleaned_data['mobile_number']


class NgProfileForm(NgModelFormMixin, NgFormValidationMixin, Bootstrap3ModelForm):
    """
    Angular model form for profile attached to a User.
    
    """
    gender = EmptyChoiceField(choices=GENDER_CHOICES, required=False, empty_label=_("Sex?"))

    class Meta:
        model = Profile
        fields = ('age', 'gender', 'country', 'region', 'city')

        # dal aka. autocomplete_light
        widgets = {
            'age': forms.NumberInput(attrs={'placeholder': _('Age')}),
            'region': NgModelSelect2(
                url='cities:region-autocomplete',
                forward=['country'],
                attrs={'data-placeholder': _("What region are you from?"),}
            ),
            'city': NgModelSelect2(
                url='cities:city-autocomplete',
                forward=['region'],
                attrs={'data-placeholder': _("Your birth place?")}
            ),

        }

    def __init__(self, *args, **kwargs):
        super(NgProfileForm, self).__init__(*args, **kwargs)

        # Empty labels for all fields
        for f in self.fields:
            self.fields[f].label = ''
            self.fields[f].help_text = ''

