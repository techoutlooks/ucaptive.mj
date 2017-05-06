# -*- coding: utf-8 -*-

from data_importer.views import DataImporterForm
from apps.accounts.models import UReportDataImporter

from django.conf import settings

from data_importer.models import FileHistory
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType


class UReportDataImporterCreateView(DataImporterForm):
    """
    Import csv, xls, xlsx data into Reporter model.

    """
    importer = UReportDataImporter
    extra_context = {'title': 'Create Form Data Importer',
                     'template_file': settings.IMPORTER_TEMPLATE_FILE}

    def form_valid(self, form, owner=None):
        if self.request.user.id:
            owner = self.request.user

        if self.importer.Meta.model:
            content_type = ContentType.objects.get_for_model(self.importer.Meta.model)
        else:
            content_type = None

        file_history, _ = FileHistory.objects.get_or_create(file_upload=form.cleaned_data['file_upload'],
                                                            owner=owner,
                                                            content_type=content_type)

        if not self.is_task or not hasattr(self.task, 'delay'):
            self.task.run(importer=self.importer,
                          source=file_history,
                          owner=owner,
                          send_email=False)
            if self.task.parser.errors:
                messages.error(self.request, self.task.parser.errors)
            else:
                messages.success(self.request,
                                 self.extra_context.get('success_message', "File uploaded successfully"))
        else:
            self.task.delay(importer=self.importer, source=file_history, owner=owner)
            if owner:
                messages.info(
                    self.request,
                    "When importer was finished one email will send to: {0!s}".format(owner.email)
                )
            else:
                messages.info(
                    self.request,
                    "Importer task in queue"
                )

        return super(DataImporterForm, self).form_valid(form)

