import logging

from datetime import datetime

from django.http import Http404
from django.db.models import Q
from django.http import HttpResponse
from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as statuses

import django_filters.rest_framework
from easy_pdf.rendering import render_to_pdf

from core.common import (
    PROGRESS_REPORT_STATUS,
    INDICATOR_REPORT_STATUS,
    OVERALL_STATUS,
)

from core.paginations import SmallPagination
from core.permissions import IsAuthenticated
from core.models import Location
from core.serializers import ShortLocationSerializer

from indicator.models import Reportable, IndicatorReport, IndicatorBlueprint
from indicator.serializers import IndicatorListSerializer, PDReportContextIndicatorReportSerializer
from indicator.filters import PDReportsFilter
from indicator.serializers import IndicatorBlueprintSimpleSerializer

from partner.models import Partner

from .serializers import (
    ProgrammeDocumentSerializer,
    ProgrammeDocumentDetailSerializer,
    ProgressReportSimpleSerializer,
    ProgressReportSerializer,
    ProgressReportReviewSerializer,
    LLOutputSerializer,
    LLOutputIndicatorsSerializer,
    ProgrammeDocumentCalculationMethodsSerializer,
    ProgrammeDocumentProgressSerializer
)

from .models import ProgrammeDocument, ProgressReport
from .filters import ProgrammeDocumentFilter, ProgressReportFilter, ProgrammeDocumentIndicatorFilter

logger = logging.getLogger(__name__)



class ProgrammeDocumentAPIView(ListAPIView):
    """
    Endpoint for getting a list of Programme Documents and being able to
    filter by them.
    """
    serializer_class = ProgrammeDocumentSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = SmallPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, )
    filter_class = ProgrammeDocumentFilter

    def get_queryset(self):
        return ProgrammeDocument.objects.filter(
            partner=self.request.user.partner)

    def list(self, request, workspace_id, *args, **kwargs):
        queryset = self.get_queryset().filter(workspace=workspace_id)
        filtered = ProgrammeDocumentFilter(request.GET, queryset=queryset)

        page = self.paginate_queryset(filtered.qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(filtered.qs, many=True)
        return Response(
            serializer.data,
            status=statuses.HTTP_200_OK
        )


class ProgrammeDocumentDetailsAPIView(RetrieveAPIView):

    serializer_class = ProgrammeDocumentDetailSerializer
    permission_classes = (IsAuthenticated, )
    lookup_url_kwarg = 'pd_id'

    def get(self, request, workspace_id, pd_id, *args, **kwargs):
        """
        Get Programme Document Details by given pk.
        """
        self.workspace_id = workspace_id
        serializer = self.get_serializer(
            self.get_object(pd_id)
        )
        return Response(serializer.data, status=statuses.HTTP_200_OK)

    def get_object(self, pd_id):
        try:
            return ProgrammeDocument.objects.get(
                partner=self.request.user.partner,
                workspace=self.workspace_id,
                pk=pd_id)
        except ProgrammeDocument.DoesNotExist as exp:
            logger.exception({
                "endpoint": "ProgrammeDocumentDetailsAPIView",
                "request.data": self.request.data,
                "pk": pd_id,
                "exception": exp,
            })
            raise Http404


class ProgrammeDocumentProgressAPIView(RetrieveAPIView):

    serializer_class = ProgrammeDocumentProgressSerializer
    permission_classes = (IsAuthenticated, )
    lookup_url_kwarg = 'pd_id'

    def get(self, request, workspace_id, pd_id, *args, **kwargs):
        """
        Get Programme Document Details by given pk.
        """
        self.workspace_id = workspace_id
        serializer = self.get_serializer(
            self.get_object(pd_id)
        )
        return Response(serializer.data, status=statuses.HTTP_200_OK)

    def get_object(self, pd_id):
        try:
            return ProgrammeDocument.objects.get(
                partner=self.request.user.partner,
                workspace=self.workspace_id,
                pk=pd_id)
        except ProgrammeDocument.DoesNotExist as exp:
            logger.exception({
                "endpoint": "ProgrammeDocumentProgressAPIView",
                "request.data": self.request.data,
                "pk": pd_id,
                "exception": exp,
            })
            raise Http404


class ProgrammeDocumentLocationsAPIView(ListAPIView):

    queryset = Location.objects.all()
    serializer_class = ShortLocationSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, workspace_id, *args, **kwargs):
        pd = ProgrammeDocument.objects.filter(partner=self.request.user.partner, workspace=workspace_id)
        queryset = self.get_queryset().filter(reportables__indicator_reports__progress_report__programme_document__in=pd).distinct()
        filtered = ProgressReportFilter(request.GET, queryset=queryset)

        page = self.paginate_queryset(filtered.qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(filtered.qs, many=True)
        return Response(
            serializer.data,
            status=statuses.HTTP_200_OK
        )

class ProgrammeDocumentIndicatorsAPIView(ListAPIView):

    queryset = Reportable.objects.filter(lower_level_outputs__isnull=False)
    serializer_class = IndicatorListSerializer
    pagination_class = SmallPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)

    def list(self, request, workspace_id, *args, **kwargs):
        """
        Return list of Reportable objects that are associated with LLO's
        of the PD's that this users partner belongs to.
        """
        pds = ProgrammeDocument.objects.filter(
            partner=self.request.user.partner, workspace=workspace_id)
        queryset = self.get_queryset().filter(
            indicator_reports__progress_report__programme_document__in=pds).distinct()
        filtered = ProgrammeDocumentIndicatorFilter(request.GET,
                                                    queryset=queryset)

        page = self.paginate_queryset(filtered.qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(filtered.qs, many=True)
        return Response(
            serializer.data,
            status=statuses.HTTP_200_OK
        )

class ProgressReportAPIView(ListAPIView):
    """
    Endpoint for getting list of all Progress Reports. Supports filtering
    as per ProgressReportFilter by status, pd_ref_title, programme_document
    (id) etc.

    Supports additional GET param to filter by external_partner_id
    """
    serializer_class = ProgressReportSimpleSerializer
    pagination_class = SmallPagination
    permission_classes = (IsAuthenticated, )
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, )
    filter_class = ProgressReportFilter

    def get_queryset(self):
        external_partner_id = self.request.GET.get('external_partner_id')
        if external_partner_id is not None:
            qset = Partner.objects.filter(external_id=external_partner_id)
            return ProgressReport.objects.filter(
                programme_document__partner__in=qset)
        else:
            # Limit reports to this user's partner only
            return ProgressReport.objects.filter(
                programme_document__partner=self.request.user.partner)

    def list(self, request, workspace_id, *args, **kwargs):
        queryset = self.get_queryset().filter(
            programme_document__workspace=workspace_id)
        filtered = ProgressReportFilter(request.GET, queryset=queryset)

        page = self.paginate_queryset(filtered.qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(filtered.qs, many=True)
        return Response(
            serializer.data,
            status=statuses.HTTP_200_OK
        )


class ProgressReportPDFView(RetrieveAPIView):
    """
        Endpoint for getting PDF of Progress Report Annex C.
    """
    permission_classes = (IsAuthenticated,)

    def prepare_reportable(self, indicator_reports):
        result = list()
        temp = None
        d = list()
        for r in indicator_reports:
            if not temp:
                temp = r.reportable.id
            elif temp != r.reportable.id:
                result.append(d)
                temp = None
                d = list()
            d.append(r)
        if d:
            result.append(d)
        return result

    def get(self, request, pk, *args, **kwargs):
        # Render to pdf
        report = ProgressReport.objects.get(id=pk)

        data = dict()

        data['unicef_office'] = report.programme_document.unicef_office
        data['title'] = report.programme_document.title
        data['reference_number'] = report.programme_document.reference_number
        data['start_date'] = report.programme_document.start_date.strftime(settings.PRINT_DATA_FORMAT)
        data['end_date'] = report.programme_document.end_date.strftime(settings.PRINT_DATA_FORMAT)
        data['cso_contribution'] = report.programme_document.cso_contribution
        data['budget'] = report.programme_document.budget
        data['funds_received_to_date'] = report.programme_document.funds_received_to_date
        data['challenges_in_the_reporting_period'] = report.challenges_in_the_reporting_period
        data['proposed_way_forward'] = report.proposed_way_forward
        data['partner_contribution_to_date'] = report.partner_contribution_to_date
        data['submission_date'] = report.get_submission_date()
        data['reporting_period'] = report.get_reporting_period()

        data['partner'] = report.programme_document.partner

        data['authorized_officer'] = report.programme_document.unicef_officers.first()
        data['focal_point'] = report.programme_document.unicef_focal_point.first()

        data['outputs'] = self.prepare_reportable(report.indicator_reports.all().order_by('reportable'))

        pdf = render_to_pdf("report_annex_c_pdf.html", data)
        return HttpResponse(pdf, content_type='application/pdf')


class ProgressReportDetailsAPIView(RetrieveAPIView):
    """
    Endpoint for getting Progress Report
    """
    serializer_class = ProgressReportSerializer
    permission_classes = (IsAuthenticated, )
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, )

    def get(self, request, workspace_id, pk, *args, **kwargs):
        """
        Get Progress Report Details by given pk.
        """
        self.workspace_id = workspace_id
        serializer = self.get_serializer(
            self.get_object(pk)
        )
        return Response(serializer.data, status=statuses.HTTP_200_OK)

    def get_object(self, pk):
        try:
            return ProgressReport.objects.get(
                programme_document__partner=self.request.user.partner,  # TODO: check if needed?
                programme_document__workspace=self.workspace_id,
                pk=pk)
        except ProgressReport.DoesNotExist as exp:
            logger.exception({
                "endpoint": "ProgressReportDetailsAPIView",
                "request.data": self.request.data,
                "pk": pk,
                "exception": exp,
            })
            raise Http404

class ProgressReportIndicatorsAPIView(ListAPIView):
    serializer_class = PDReportContextIndicatorReportSerializer
    pagination_class = SmallPagination
    permission_classes = (IsAuthenticated,)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = PDReportsFilter

    def get_queryset(self):
        # Limit reports to partner only
        return IndicatorReport.objects.filter(progress_report__programme_document__partner=self.request.user.partner)

    def list(self, request, workspace_id, progress_report_id, *args, **kwargs):
        """
        Get Programme Document Details by given pk.
        """
        queryset = self.get_queryset().filter(progress_report__id=progress_report_id, progress_report__programme_document__workspace=workspace_id)
        filtered = PDReportsFilter(request.GET, queryset=queryset)

        page = self.paginate_queryset(filtered.qs)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(filtered.qs, many=True)
        return Response(serializer.data, status=statuses.HTTP_200_OK)


class ProgressReportLocationsAPIView(ListAPIView):
    queryset = Location.objects.all()
    serializer_class = ShortLocationSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return ProgressReport.objects.get(programme_document__partner=self.request.user.partner, programme_document__workspace=self.workspace_id, pk=pk)
        except ProgressReport.DoesNotExist as exp:
            logger.exception({
                "endpoint": "ProgressReportLocationsAPIView",
                "request.data": self.request.data,
                "pk": pk,
                "exception": exp,
            })
            raise Http404

    def list(self, request, workspace_id, progress_report_id, *args, **kwargs):
        self.workspace_id = workspace_id
        pr = self.get_object(progress_report_id)
        queryset = self.get_queryset().filter(
            indicator_location_data__indicator_report__progress_report=pr).distinct()
        filtered = ProgressReportFilter(request.GET, queryset=queryset)

        page = self.paginate_queryset(filtered.qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(filtered.qs, many=True)
        return Response(
            serializer.data,
            status=statuses.HTTP_200_OK
        )


class ProgressReportSubmitAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return ProgressReport.objects.get(
                programme_document__partner=self.request.user.partner,
                programme_document__workspace=self.workspace_id,
                pk=pk)
        except ProgressReport.DoesNotExist as exp:
            logger.exception({
                "endpoint": "ProgressReportSubmitAPIView",
                "request.data": self.request.data,
                "pk": pk,
                "exception": exp,
            })
            raise Http404

    @transaction.atomic
    def post(self, request, workspace_id, pk, *args, **kwargs):
        self.workspace_id = workspace_id
        progress_report = self.get_object(pk)

        for ir in progress_report.indicator_reports.all():
            # Check if all indicator data is fulfilled for IR status different then Met or No Progress
            if ir.overall_status not in (OVERALL_STATUS.met, OVERALL_STATUS.no_progress):
                for data in ir.indicator_location_data.all():
                    for key, vals in data.disaggregation.iteritems():
                        if ir.is_percentage and (vals.get('c', None) in [None, '']):
                            _errors = [{
                                "message": "You have not completed all required indicators for this progress report. Unless your Output status is Met or has No Progress, all indicator data needs to be completed."}]
                            return Response({"errors": _errors},
                                            status=statuses.HTTP_400_BAD_REQUEST)
                        elif ir.is_number and (vals.get('v', None) in [None, '']):
                            _errors = [{
                                "message": "You have not completed all required indicators for this progress report. Unless your Output status is Met or has No Progress, all indicator data needs to be completed."}]
                            return Response({"errors": _errors},
                                            status=statuses.HTTP_400_BAD_REQUEST)

            # Check if indicator was already submitted or SENT BACK
            if ir.submission_date is None or ir.report_status == INDICATOR_REPORT_STATUS.sent_back:
                ir.submission_date = datetime.now().date()
                ir.report_status = INDICATOR_REPORT_STATUS.submitted
                ir.save()

        if progress_report.submission_date is None or progress_report.status == PROGRESS_REPORT_STATUS.sent_back:
            progress_report.status = PROGRESS_REPORT_STATUS.submitted
            progress_report.submission_date = datetime.now().date()
            progress_report.submitted_by = self.request.user
            progress_report.save()
            serializer = ProgressReportSerializer(instance=progress_report)
            return Response(serializer.data, status=statuses.HTTP_200_OK)
        else:
            _errors = [{
                           "message": "Progress report was already submitted. Your IMO will need to send it back for you to edit your submission."}]
            return Response({"errors": _errors},
                            status=statuses.HTTP_400_BAD_REQUEST)


class ProgressReportReviewAPIView(APIView):
    """
    Called by PO to accept or send back a submitted progress report. Called
    from outside of PRP.

    Only a PO (not a partner user) should be allowed to do this action.
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return ProgressReport.objects.get(
                programme_document__workspace=self.workspace_id,
                pk=pk)
        except ProgressReport.DoesNotExist as exp:
            logger.exception({
                "endpoint": "ProgressReportReviewAPIView",
                "request.data": self.request.data,
                "pk": pk,
                "exception": exp,
            })
            raise Http404

    @transaction.atomic
    def post(self, request, workspace_id, pk, *args, **kwargs):
        """
        Only if the progress report is in submitted state that this POST
        request will be successful.
        """
        self.workspace_id = workspace_id
        progress_report = self.get_object(pk)

        if progress_report.status != PROGRESS_REPORT_STATUS.submitted:
            _errors = [{"message": "This report is not in submitted state."}]
            return Response({"errors": _errors},
                            status=statuses.HTTP_400_BAD_REQUEST)

        serializer = ProgressReportReviewSerializer(data=request.data)
        if serializer.is_valid():
            progress_report.status = serializer.validated_data['status']
            progress_report.review_date = datetime.now().date()
            if progress_report.status == PROGRESS_REPORT_STATUS.sent_back:
                progress_report.sent_back_feedback = serializer.validated_data[
                    'comment']
            progress_report.save()
            serializer = ProgressReportSerializer(instance=progress_report)
            return Response(serializer.data, status=statuses.HTTP_200_OK)

        return Response({"errors": serializer.errors},
                        status=statuses.HTTP_400_BAD_REQUEST)


class ProgrammeDocumentCalculationMethodsAPIView(APIView):
    """
    Supports GET request to get the unit and calculation for each indicator
    grouped by LLO for a particular PD.

    POST request takes same format data to update the calculation methods then.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ProgrammeDocumentCalculationMethodsSerializer

    def get(self, request, workspace_id, pd_id):
        """
        Construct the input data to the serializer for the LLO and its
        associated indicators.
        """
        pd = get_object_or_404(ProgrammeDocument,
                               id=pd_id,
                               workspace__id=workspace_id)

        data = {'ll_outputs_and_indicators': []}
        for llo in pd.lower_level_outputs:
            indicator_blueprints = []
            for reportable in llo.reportables.all():
                indicator_blueprints.append(reportable.blueprint)

            inner_data = {}
            inner_data['ll_output'] = LLOutputSerializer(instance=llo).data
            inner_data['indicators'] = IndicatorBlueprintSimpleSerializer(
                indicator_blueprints, many=True).data

            data['ll_outputs_and_indicators'].append(inner_data)

        return Response(ProgrammeDocumentCalculationMethodsSerializer(
            data).data)

    @transaction.atomic
    def post(self, request, workspace_id, pd_id, *args, **kwargs):
        """
        The goal of this is to set the calculation methods for the indicators
        associated with lower level outputs of this PD.
        """
        serializer = ProgrammeDocumentCalculationMethodsSerializer(
            data=request.data)
        if serializer.is_valid():
            print serializer.validated_data
            for llo_and_indicators in serializer.validated_data[
                    'll_outputs_and_indicators']:
                for indicator_blueprint in llo_and_indicators['indicators']:
                    print indicator_blueprint
                    instance = get_object_or_404(IndicatorBlueprint,
                                                 id=indicator_blueprint['id'])
                    instance.calculation_formula_across_periods = \
                        indicator_blueprint[
                            'calculation_formula_across_periods']
                    instance.calculation_formula_across_locations = \
                        indicator_blueprint[
                            'calculation_formula_across_locations']
                    instance.clean()
                    instance.save()
            return Response(serializer.data, status=statuses.HTTP_200_OK)

        return Response({"errors": serializer.errors},
                        status=statuses.HTTP_400_BAD_REQUEST)
