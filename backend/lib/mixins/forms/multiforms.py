# -*- coding: utf-8 -*-
"""
Validate mulitple forms in a single formView class Django
Credits: https://gist.github.com/michelts/1029336

Usage:

    class NewUserView(MultipleFormsView):
        template_name = 'users/user_form.html'
        form_classes = {
            'newuser': NewUserForm,
            'newidea': NewIdeaForm,
        }
    
Get these in template using: 
    {{ forms.newuser.as_ul }}
    {{ forms.newidea.as_ul }}

    
"""

from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.edit import FormMixin, ProcessFormView


class MultipleFormsMixin(FormMixin):
    """
    A mixin that provides a way to show and handle several forms in a
    request.
    """
    form_classes = {} # set the form classes as a mapping

    def get_form_classes(self):
        return self.form_classes

    def get_forms(self, form_classes):
        """
        Initializes the forms defined in `form_classes` with initial data from `get_initial()` and
        kwargs from get_form_kwargs().
        """
        initial = self.get_initial()
        kwargs = self.get_form_kwargs()
        return dict([(key, form_class(initial=initial[key], **kwargs[key])) \
            for key, form_class in form_classes.items()])

    def forms_valid(self, forms):
        return super(MultipleFormsMixin, self).form_valid(forms)

    def forms_invalid(self, forms):
        return self.render_to_response(self.get_context_data(forms=forms))

    # below being debbuged
    # https://github.com/TimBest/django-multi-form-view/blob/master/multi_form_view/base.py

    def get_form_kwargs(self):
        """
        Build the keyword arguments required to instantiate the form.
        """
        kwargs = {}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_initial(self):
        """ 
        Returns a copy of `initial` with empty initial data dictionaries for each form.
        """
        initial = super(MultipleFormsMixin, self).get_initial()
        for key in self.form_classes.iterkeys():
            initial[key] = {}
        return initial

    def get_context_data(self, **kwargs):
        """
        Add forms into the context dictionary.
        """
        context = {}
        if 'forms' not in kwargs:
            context['forms'] = self.get_forms()
        else:
            context['forms'] = kwargs['forms']

        return context


class ProcessMultipleFormsView(ProcessFormView):
    """
    A mixin that processes multiple forms on POST. Every form must be
    valid.
    """
    def get(self, request, *args, **kwargs):
        form_classes = self.get_form_classes()
        forms = self.get_forms(form_classes)
        return self.render_to_response(self.get_context_data(forms=forms))

    def post(self, request, *args, **kwargs):
        form_classes = self.get_form_classes()
        forms = self.get_forms(form_classes)
        if all([form.is_valid() for form in forms.values()]):
            return self.forms_valid(forms)
        else:
            return self.forms_invalid(forms)


class BaseMultipleFormsView(MultipleFormsMixin, ProcessMultipleFormsView):
    """
    A base view for displaying several forms.
    """


class MultipleFormsView(TemplateResponseMixin, BaseMultipleFormsView):
    """
    A view for displaying several forms, and rendering a template response.
    """