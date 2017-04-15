# -*- coding: utf-8 -*-
"""
django-angular views mixins library.

Usage:
    from djng.forms import NgFormValidationMixin, NgModelFormMixin
    from djng.styling.bootstrap3.forms import Bootstrap3Form, Bootstrap3ModelForm
    from lib.mixins.views.angular import NgFormViewMixin

    class MyForm(NgModelFormMixin, NgFormValidationMixin, Bootstrap3Form):
        pass
    
    class MyFormView(NgFormViewMixin, FormView):
        form_class = MyForm

"""


class NgFormViewMixin(object):
    """
    Pass arguments to djng.forms.* forms instances right inside of url_patterns.
    # eg.: url(r'^signin/$', views.MyFormView.as_view(scope_prefix='credentials'), name='ng-login'),

    """
    # view kwargs
    scope_prefix = None
    controller_as = '$ctrl'

    def get_form_kwargs(self):
        kwargs = super(NgFormViewMixin, self).get_form_kwargs()

        if self.scope_prefix or self.controller_as:
            kwargs.update({
                'scope_prefix': ".".join([self.controller_as, self.scope_prefix])
            })
        return kwargs