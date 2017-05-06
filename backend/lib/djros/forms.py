# -*- coding: utf-8 -*-
__author__ = 'ceduth'


from django.forms.models import ModelForm
from .helpers import booleanify
from .models import Cap


class CapForm(ModelForm):
    class Meta:
        model = Cap
        fields = '__all__'

    def clean_disabled(self):
        return booleanify(self.cleaned_data.get('disabled'))

    def clean_running(self):
        return booleanify(self.cleaned_data.get('running'))

    def clean_inactive(self):
        return booleanify(self.cleaned_data.get('inactive'))

    def clean_bound(self):
        return booleanify(self.cleaned_data.get('bound'))



