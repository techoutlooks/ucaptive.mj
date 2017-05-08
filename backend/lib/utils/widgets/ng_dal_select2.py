from django.forms.widgets import Select
from dal_select2.widgets import Select2WidgetMixin
from dal.widgets import QuerySetSelectMixin


class NgSelect(Select):

    def render(self, name, value, attrs=None, choices=()):

        controller_as = "$ctrl"
        scope_prefix = "profile"

        ng_model = "{}.{}['{}']".format(controller_as, scope_prefix, name)
        ng_choices = "$ctrl.{}s".format(name)
        ng_selected = ""

        # attrs['ng-init'] = "{}={}[0]".format(ng_model, ng_choices)
        attrs['ng-options'] = "choice.id as choice.text for choice in {choices} track by choice.id {selected}"\
            .format(choices=ng_choices, selected=ng_selected)
        attrs['ng-change'] = "{}.{}Changed()".format(controller_as, name)
        return super(NgSelect, self).render(name, value, attrs=attrs, choices=choices)

    def render_options(self, choices, selected_choices):
        """ ng-options already renders our <options/> """
        return ""


class NgModelSelect2(QuerySetSelectMixin,
                     Select2WidgetMixin,
                     NgSelect):
    """Select widget for QuerySet choices and Select2."""
