from django.test import TestCase

from .models import Reporter
from django.db.models import Q

class ModelFactoryModelTest(TestCase):

    kwargs = {'first_name': 'Alpha', 'mobile_number': '+224628340054'}
    fk_name = 'mobile_number'
    model = Reporter
    match='icontains'

    def test_get_fk_instance(self):
        """
        Given a fk field name in 'model', return fk instance that matches the criteria,
        if found, or None. Applies to this model (cls) if no model given.
        """

        opts = {}
        for prop in self.kwargs.keys(): opts.update({"%s__{}".format(self.match) % prop: self.kwargs.get(prop)})
        print "get_fk_instance:: model=%s fk_name=%s opts=%s" %(self.model, self.fk_name, opts)

        obj = self.model.objects.filter(Q(**opts)).first()
        print obj
        
        self.assertTrue(isinstance(obj, Reporter))


