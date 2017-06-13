# test xls file to model importer

from apps.accounts.models import UReportDataImporter
source = '../data/fixtures/ureporters_mj-04262017.xls'
imp = UReportDataImporter(source=source)
imp.save()

# or via task

from data_importer.tasks import DataImpoterTask
from apps.accounts.models import UReportDataImporter
source = '/home/ceduth/Documents/Devl/Python/Projects/ucaptive.mj/data/fixtures/ureporters_mj-04262017.xls'
u = Reporter.objects.first()
t = DataImpoterTask()
t.run(importer=UReportDataImporter, source=source, owner=u, message='Posting Task ...')

