# -*- coding: utf-8 -*-
"""
Custom form to register a U-Reporter.

"""
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from registration.forms import RegistrationForm

from djng.styling.bootstrap3.forms import Bootstrap3Form
from djng.forms import NgFormValidationMixin, NgModelFormMixin
from djng.styling.bootstrap3.forms import Bootstrap3ModelForm

from accounts.models import Reporter


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

    username = forms.RegexField(r'^\+?[0-9 .-]{9,15}$', required=True, label='',
                                     widget=forms.TextInput(attrs={'placeholder': _('Mobile Number')}),
                                     error_messages={'invalid': _('Phone number have 9-14 digits and may start with +')})
    password = forms.CharField(required=True, label='',
                               widget=forms.PasswordInput(attrs={'placeholder': _('Password')}),
                               validators=[validate_password])

    # help_text=_('Your password should contain more than 6 alphanumeric characters !'))

    class Meta:
        fields = ('username', 'password',)


class NgRegistrationForm(NgModelFormMixin, NgFormValidationMixin, Bootstrap3ModelForm):
    """
    Subclass of ``RegistrationForm`` which enforces uniqueness of phone number.

    """
    username = forms.RegexField(r'^\+?[0-9 .-]{9,15}$', required=True, label='',
                                     widget=forms.TextInput(attrs={'placeholder': _('Mobile Number')}),
                                     error_messages={'invalid': _('Phone number have 9-14 digits and may start with +')})
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
        super(NgRegistrationForm, self).__init__(*args, **kwargs)

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
