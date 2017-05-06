from django import forms
from django.utils.translation import ugettext_lazy as _

from djng.styling.bootstrap3.forms import Bootstrap3Form, Bootstrap3ModelForm
from djng.forms import NgFormValidationMixin
from djng.forms import NgModelFormMixin

from ..freeradius.models import RadUser


class RadUserFilterForm(NgFormValidationMixin, Bootstrap3Form):
    username = forms.CharField(required=False)
    is_active = forms.ChoiceField(choices=[('-1', 'Any'), ('1', 'Active'), ('0', 'Suspended')], initial="-1")
    is_online = forms.ChoiceField(choices=[('-1', 'Any'), ('0', 'Offline'), ('1', 'Online')], initial="-1")
    #group = forms.CharField(required=False)


class RadUserForm(NgModelFormMixin, NgFormValidationMixin, Bootstrap3ModelForm):
    username = forms.RegexField(r'^\+?[0-9 .-]{9,14}$',
                                widget=forms.TextInput(attrs={'readonly':'readonly'}),
                                min_length=3, max_length=20, required=True,
                                error_messages={'invalid' : _('Only letters, digests and .@-_ are allowed.')})
    password = forms.CharField(max_length=20)
    is_active = forms.BooleanField(required=False, initial=True)
    groups = forms.RegexField(r'^[0-9a-zA-Z\._,]+$', max_length=50, initial='default', required=False,
                              help_text=_('comma seprated group list, no space; eg "default,test"'),
                              error_messages={'invalid' : _('Only letters, digests and ._ are allowed as group name.')})

    class Meta:
        model = RadUser
        fields = ('username', 'password', 'is_active', 'groups')

    def clean_groups(self):
        data = self.cleaned_data['groups']
        data = u','.join([x for x in data.split(u',') if x])
        return data


class NewRadUserForm(RadUserForm):
    username = forms.RegexField(r'^\+?[0-9 .-]{9,14}$',
                                min_length=3, max_length=20, required=True,
                                error_messages={'invalid' : _('Only letters, digests and .@-_ are allowed.')})
 

class RadGroupForm(NgFormValidationMixin, Bootstrap3Form):
    groupname = forms.RegexField(r'^[0-9a-zA-Z\-_]+$', 
                                min_length=3, max_length=20, required=True,
                                error_messages={'invalid' : _('Only letters, digests and -_ are allowed.')})
    simultaneous_use = forms.IntegerField(initial=1)


class NewRadGroupForm(RadGroupForm):
    groupname = forms.RegexField(r'^[0-9a-zA-Z\-_]+$', 
                                min_length=3, max_length=20, required=True,
                                error_messages={'invalid' : _('Only letters, digests and -_ are allowed.')})
