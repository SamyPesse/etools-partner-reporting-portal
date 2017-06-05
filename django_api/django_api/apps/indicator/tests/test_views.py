from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from account.models import User
from core.factories import (
    IndicatorReportFactory, ProgrammeDocumentFactory, ReportableToLowerLevelOutputFactory,
    ProgressReportFactory,
    SectionFactory,
    IndicatorLocationDataFactory,
)
from indicator.models import IndicatorReport

from unicef.models import LowerLevelOutput, Section, ProgrammeDocument


class TestPDReportsAPIView(APITestCase):

    def setUp(self):
        self.quantity = 5

        ProgrammeDocumentFactory.create_batch(self.quantity)
        print "{} ProgrammeDocument objects created".format(self.quantity)

        SectionFactory.create_batch(self.quantity)
        print "{} Section objects created".format(self.quantity)

        # Linking the followings:
        # created LowerLevelOutput - ReportableToLowerLevelOutput
        # Section - ProgrammeDocument via ReportableToLowerLevelOutput
        # ProgressReport - IndicatorReport from ReportableToLowerLevelOutput
        # IndicatorReport & Location from ReportableToLowerLevelOutput - IndicatorLocationData
        for idx in xrange(self.quantity):
            llo = LowerLevelOutput.objects.all()[idx]
            reportable = ReportableToLowerLevelOutputFactory(content_object=llo)

            reportable.content_object.indicator.programme_document.sections.add(Section.objects.all()[idx])

            indicator_report = reportable.indicator_reports.first()
            indicator_report.progress_report = ProgressReportFactory()
            indicator_report.save()

            indicator_location_data = IndicatorLocationDataFactory(indicator_report=indicator_report, location=reportable.locations.first())

        # Make all requests in the context of a logged in session.
        admin, created = User.objects.get_or_create(username='admin', defaults={
            'email': 'admin@unicef.org',
            'is_superuser': True,
            'is_staff': True
        })
        admin.set_password('Passw0rd!')
        admin.save()
        self.client = APIClient()
        self.client.login(username='admin', password='Passw0rd!')

    def test_list_api(self):
        pd = ProgrammeDocument.objects.first()
        url = reverse('programme-document-reports', kwargs={'pd_id': pd.pk})
        response = self.client.get(url, format='json')

        self.assertTrue(status.is_success(response.status_code))

        pd = ProgrammeDocument.objects.get(pk=pd.id)
        pks = pd.reportable_queryset.values_list('indicator_reports__pk', flat=True)

        first_ir = IndicatorReport.objects.filter(id__in=pks).first()
        filter_url = "%s?status=%s" % (
            url,
            first_ir.progress_report.get_status_display()
        )
        response = self.client.get(filter_url, format='json')
        self.assertTrue(status.is_success(response.status_code))


class TestIndicatorListAPIView(APITestCase):

    def setUp(self):
        self.quantity = 5

        ProgrammeDocumentFactory.create_batch(self.quantity)
        print "{} ProgrammeDocument objects created".format(self.quantity)

        SectionFactory.create_batch(self.quantity)
        print "{} Section objects created".format(self.quantity)

        # Linking the followings:
        # created LowerLevelOutput - ReportableToLowerLevelOutput
        # Section - ProgrammeDocument via ReportableToLowerLevelOutput
        # ProgressReport - IndicatorReport from ReportableToLowerLevelOutput
        # IndicatorReport & Location from ReportableToLowerLevelOutput - IndicatorLocationData
        for idx in xrange(self.quantity):
            llo = LowerLevelOutput.objects.all()[idx]
            reportable = ReportableToLowerLevelOutputFactory(content_object=llo)

            reportable.content_object.indicator.programme_document.sections.add(Section.objects.all()[idx])

            indicator_report = reportable.indicator_reports.first()
            indicator_report.progress_report = ProgressReportFactory()
            indicator_report.save()

            indicator_location_data = IndicatorLocationDataFactory(indicator_report=indicator_report, location=reportable.locations.first())

    def test_list_api(self):
        url = reverse('indicator-list-create-api')
        response = self.client.get(url, format='json')

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data['results']), self.quantity)
