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
    AngularJS ControllerAs FormView
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


class NgMultipleFormsViewMixin(object):
    """
    AngularJS ControllerAs FormView. Use with ceduth.helpers.mixins.multiforms.MultipleFormsView
    Pass arguments to djng.forms.* forms instances right inside of url_patterns.
    # eg.: url(r'^signin/$', views.MyFormView.as_view(scope_prefix='credentials'), name='ng-login'),

    """
    form_name = None            # name of the unique form container used to embed for all forms.
    scope_prefixes = None       # angular scope prefix per form. dict of form_id,scope_prefix values.
    controller_as = '$ctrl'     # angular controller instance.

    def get_form_kwargs(self):
        """ 
        Set scope-prefix, ie. kwargs respective to each form prefixed by a unique controller_as.
        """
        kwargs = dict([(key,{}) for key in self.form_classes.iterkeys()])
        if self.scope_prefixes or self.controller_as:
            for key, form_class in self.form_classes.iteritems():
                kwargs[key] = super(NgMultipleFormsViewMixin, self).get_form_kwargs()
                kwargs[key].update({
                    'scope_prefix': ".".join([self.controller_as,
                                              self.scope_prefixes.get(key, getattr(form_class, 'scope_prefix', None))]),
                    'form_name': self.form_name
                })

        return kwargs

    def get_context_data(self, **kwargs):
        """
        Add forms into the context dictionary.
        """
        context = super(NgMultipleFormsViewMixin, self).get_context_data(**kwargs)
        context.update({'form_name': self.form_name})
        return context