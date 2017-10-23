from django.conf import settings
from rest_framework import serializers

from .models import ProgrammeDocument, Section, ProgressReport, Person, \
    LowerLevelOutput, PDResultLink

from core.common import PROGRESS_REPORT_STATUS, OVERALL_STATUS, CURRENCIES
from core.models import Workspace

from indicator.serializers import (
    PDReportContextIndicatorReportSerializer,
    IndicatorBlueprintSimpleSerializer,
    IndicatorLLoutputsSerializer,
    ReportableSimpleSerializer
)

from partner.models import Partner


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('name', 'title', 'email', 'phone_number')


class ProgrammeDocumentSerializer(serializers.ModelSerializer):

    id = serializers.SerializerMethodField()
    status = serializers.CharField(source='get_status_display')
    total_unicef_supplies = serializers.SerializerMethodField()
    total_unicef_supplies_currency = serializers.SerializerMethodField()
    budget_currency = serializers.SerializerMethodField()
    cso_contribution_currency = serializers.SerializerMethodField()
    funds_received_to_date_currency = serializers.SerializerMethodField()
    unicef_officers = PersonSerializer(read_only=True, many=True)
    unicef_focal_point = PersonSerializer(read_only=True, many=True)
    partner_focal_point = PersonSerializer(read_only=True, many=True)
    document_type_display = serializers.CharField(
            source='get_document_type_display')


    class Meta:
        model = ProgrammeDocument
        fields = (
            'id',
            'agreement',
            'reference_number',
            'title',
            'unicef_office',
            'start_date',
            'end_date',
            'population_focus',
            'status',
            'document_type',
            'document_type_display',
            'calculated_budget',
            'budget',
            'budget_currency',
            'cso_contribution',
            'cso_contribution_currency',
            'total_unicef_cash',
            'total_unicef_cash_currency',
            'funds_received_to_date',
            'funds_received_to_date_currency',
            'funds_received_to_date_percentage',
            'total_unicef_supplies',
            'total_unicef_supplies_currency',
            'partner_focal_point',
            'unicef_focal_point',
            'unicef_officers'
        )

    def get_id(self, obj):
        return str(obj.id)

    def get_total_unicef_supplies(self, obj):
        return str(obj.in_kind_amount)

    def get_total_unicef_supplies_currency(self, obj):
        return obj.in_kind_amount_currency

    def get_budget_currency(self, obj):
        return obj.budget_currency

    def get_cso_contribution_currency(self, obj):
        return obj.cso_contribution_currency

    def get_funds_received_to_date_currency(self, obj):
        return obj.funds_received_to_date_currency


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('name', )


class ProgrammeDocumentDetailSerializer(serializers.ModelSerializer):

    document_type = serializers.CharField(source='get_document_type_display')
    # status is choice field on different branch with migration #23 - should be uncomment when it will be merged
    # status = serializers.CharField(source='get_status_display')
    frequency = serializers.CharField(source='get_frequency_display')
    # sections = serializers.SerializerMethodField()
    sections = SectionSerializer(read_only=True, many=True)
    unicef_officers = PersonSerializer(read_only=True, many=True)
    unicef_focal_point = PersonSerializer(read_only=True, many=True)
    partner_focal_point = PersonSerializer(read_only=True, many=True)

    class Meta:
        model = ProgrammeDocument
        fields = (
            'id',
            'agreement',
            'document_type',
            'reference_number',
            'title',
            'unicef_office',
            'unicef_officers',
            'unicef_focal_point',
            'partner_focal_point',
            'start_date',
            'end_date',
            'population_focus',
            # 'status',
            'frequency',
            'sections',
        )


class LLOutputSerializer(serializers.ModelSerializer):
    """
    Nests with LL output.
    """

    class Meta:
        model = LowerLevelOutput
        fields = (
            'id',
            'title',
        )


class CPOutputSerializer(serializers.ModelSerializer):
    """
    Nests with CP output
    """
    ll_outputs = LLOutputSerializer(many=True, read_only=True)

    class Meta:
        model = PDResultLink
        fields = (
            'id',
            'title',
            'll_outputs',
            'external_cp_output_id',
        )


class ProgrammeDocumentOutputSerializer(serializers.ModelSerializer):
    """
    Serializer for PD with indicator reports nested by output.
    """
    cp_outputs = CPOutputSerializer(many=True, read_only=True)

    class Meta:
        model = ProgrammeDocument
        fields = (
            'id',
            'title',
            'cp_outputs',
        )


class ProgressReportSimpleSerializer(serializers.ModelSerializer):
    programme_document = ProgrammeDocumentSerializer()
    reporting_period = serializers.SerializerMethodField()
    is_draft = serializers.SerializerMethodField()
    review_overall_status_display = serializers.CharField(
            source='get_review_overall_status_display')

    class Meta:
        model = ProgressReport
        fields = (
            'id',
            'partner_contribution_to_date',
            'challenges_in_the_reporting_period',
            'proposed_way_forward',
            'status',
            'reporting_period',
            'submission_date',
            'due_date',
            'is_draft',
            'review_date',
            'review_overall_status',
            'review_overall_status_display',
            'sent_back_feedback',
            'programme_document',
        )

    def get_reporting_period(self, obj):
        return "%s - %s " % (
            obj.start_date.strftime(settings.PRINT_DATA_FORMAT),
            obj.end_date.strftime(settings.PRINT_DATA_FORMAT)
        )

    def get_is_draft(self, obj):
        return obj.latest_indicator_report.is_draft if obj.latest_indicator_report else None


class ProgressReportSerializer(ProgressReportSimpleSerializer):
    programme_document = ProgrammeDocumentOutputSerializer()
    indicator_reports = serializers.SerializerMethodField()
    review_overall_status_display = serializers.CharField(
            source='get_review_overall_status_display')

    def __init__(self, llo_id=None, location_id=None, *args, **kwargs):
        self.llo_id = llo_id
        self.location_id = location_id

        super(ProgressReportSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = ProgressReport
        fields = (
            'id',
            'partner_contribution_to_date',
            'challenges_in_the_reporting_period',
            'proposed_way_forward',
            'status',
            'reporting_period',
            'submission_date',
            'due_date',
            'is_draft',
            'review_date',
            'review_overall_status',
            'review_overall_status_display',
            'sent_back_feedback',
            'programme_document',
            'indicator_reports'
        )

    def get_indicator_reports(self, obj):
        qset = obj.indicator_reports.all()
        if self.llo_id and self.llo_id is not None:
            qset = qset.filter(reportable__object_id=self.llo_id)
        if self.location_id and self.llo_id is not None:
            qset = qset.filter(reportable__locations__id=self.location_id)
        return PDReportContextIndicatorReportSerializer(
            instance=qset, read_only=True, many=True).data

    def get_reporting_period(self, obj):
        return "%s - %s " % (
            obj.start_date.strftime(settings.PRINT_DATA_FORMAT),
            obj.end_date.strftime(settings.PRINT_DATA_FORMAT)
        )

    def get_is_draft(self, obj):
        return obj.latest_indicator_report.is_draft


class ProgressReportUpdateSerializer(serializers.ModelSerializer):

    partner_contribution_to_date = serializers.CharField(required=False)
    challenges_in_the_reporting_period = serializers.CharField(required=False)
    proposed_way_forward = serializers.CharField(required=False)

    class Meta:
        model = ProgressReport
        fields = (
            'id',
            'partner_contribution_to_date',
            'challenges_in_the_reporting_period',
            'proposed_way_forward',
        )


class ProgressReportReviewSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=[
        PROGRESS_REPORT_STATUS.sent_back,
        PROGRESS_REPORT_STATUS.accepted
    ])
    comment = serializers.CharField(required=False)
    overall_status = serializers.ChoiceField(required=False,
                                             choices=OVERALL_STATUS)

    def validate(self, data):
        """
        Make sure status is only accepted or sent back. Also overall_status
        should be set if accepting
        """
        if data['status'] not in [PROGRESS_REPORT_STATUS.sent_back,
                                  PROGRESS_REPORT_STATUS.accepted]:
            raise serializers.ValidationError(
                    'Report status should be accepted or sent back')
        if data.get('overall_status', None) == OVERALL_STATUS.no_status:
            raise serializers.ValidationError('Invalid overall status')
        if data.get('status', None) == PROGRESS_REPORT_STATUS.accepted and data.get(
                'overall_status', None) is None:
            raise serializers.ValidationError(
                'Overall status required when accepting a report')
        if data.get('status', None) == PROGRESS_REPORT_STATUS.sent_back and data.get(
                'comment') is None:
            raise serializers.ValidationError(
                'Comment required when sending back report')

        return data


class LLOutputSerializer(serializers.ModelSerializer):
    # id added explicitely here since it gets stripped out from validated_dat
    # as its read_only. https://stackoverflow.com/questions/36473795/django-rest-framework-model-id-field-in-nested-relationship-serializer
    id = serializers.IntegerField()

    class Meta:
        model = LowerLevelOutput
        fields = (
            'id',
            'title'
        )


class LLOutputIndicatorsSerializer(serializers.Serializer):
    """
    Represents indicators grouped by LLO.
    """
    ll_output = LLOutputSerializer()
    indicators = IndicatorBlueprintSimpleSerializer(many=True)


class ProgrammeDocumentCalculationMethodsSerializer(serializers.Serializer):
    """
    To serialize data needed when viewing/setting calculation methods on
    indicators for a PD.
    """
    ll_outputs_and_indicators = LLOutputIndicatorsSerializer(many=True)


class ProgrammeDocumentProgressSerializer(serializers.ModelSerializer):
    """
    Serializer to show the progoress of a PD. This includes information
    around the CP output, LL output, and the latest progress report and its
    associated indicator reports as well.
    """
    frequency = serializers.CharField(source='get_frequency_display')
    sections = SectionSerializer(read_only=True, many=True)
    details = serializers.SerializerMethodField()
    latest_accepted_pr = serializers.SerializerMethodField()
    latest_accepted_pr_indicator_reports = serializers.SerializerMethodField()

    class Meta:
        model = ProgrammeDocument
        fields = (
            'id',
            'reference_number',
            'title',
            'start_date',
            'end_date',
            'frequency',
            'sections',
            'details',
            'latest_accepted_pr',
            'latest_accepted_pr_indicator_reports',
        )

    def get_details(self, obj):
        return ProgrammeDocumentOutputSerializer(obj).data

    def get_latest_accepted_pr(self, obj):
        qset = ProgressReport.objects.filter(
                status=PROGRESS_REPORT_STATUS.accepted).order_by('-end_date')
        if qset:
            return ProgressReportSimpleSerializer(
                instance=qset[0], read_only=True).data
        else:
            return {}

    def get_latest_accepted_pr_indicator_reports(self, obj):
        """
        Return data about the latest accepted indicator report associated
        with this PD (if any).
        """
        qset = ProgressReport.objects.filter(
                status=PROGRESS_REPORT_STATUS.accepted).order_by('-end_date')
        if qset:
            return PDReportContextIndicatorReportSerializer(
                instance=qset[0].indicator_reports.all(),
                read_only=True, many=True).data
        else:
            return []

# PMP API Serializers

class PMPPDPersonSerializer(serializers.ModelSerializer):

    phone_num = serializers.CharField(source='phone_number', required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Person
        fields = (
            "name",
            "title",
            "phone_num",
            "email",
        )


class PMPPDPartnerSerializer(serializers.ModelSerializer):

    name = serializers.CharField(source='title')
    short_name = serializers.CharField(source='short_title', allow_blank=True)
    unicef_vendor_number = serializers.CharField(source='vendor_number')

    class Meta:
        model = Partner
        fields = (
            "name",
            "short_name",
            "unicef_vendor_number",
        )
        validators = []

class PMPProgrammeDocumentSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='external_id')
    offices = serializers.CharField(source='unicef_office')
    number = serializers.CharField(source='reference_number')
    cso_budget = serializers.CharField(source='budget')
    unicef_budget = serializers.CharField(source='total_unicef_cash')
    funds_received = serializers.CharField(source='funds_received_to_date')
    cso_budget_currency = serializers.ChoiceField(choices=CURRENCIES, allow_null=True, source="budget_currency")
    funds_received_currency = serializers.ChoiceField(choices=CURRENCIES, allow_null=True, source="funds_received_to_date_currency")
    unicef_budget_currency = serializers.ChoiceField(choices=CURRENCIES, allow_null=True, source="total_unicef_cash_currency")
    start_date = serializers.DateField(required=False, allow_null=True)
    end_date = serializers.DateField(required=False, allow_null=True)
    partner = serializers.PrimaryKeyRelatedField(queryset=Partner.objects.all())
    workspace = serializers.PrimaryKeyRelatedField(queryset=Workspace.objects.all())

    def update(self, instance, validated_data):
        return ProgrammeDocument.objects.filter(external_id=validated_data['external_id']).update(**validated_data)

    def create(self, validated_data):
        return ProgrammeDocument.objects.create(**validated_data)

    class Meta:
        model = ProgrammeDocument
        fields = (
            "id",
            "title",
            "offices",
            "number",
            "partner",
            "start_date",
            "end_date",
            "cso_budget",
            "cso_budget_currency",
            "unicef_budget",
            "unicef_budget_currency",
            "funds_received",
            "funds_received_currency",
            "workspace",
        )

class PMPLLOSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='external_id')
    cp_output = serializers.PrimaryKeyRelatedField(queryset=PDResultLink.objects.all())

    class Meta:
        model = LowerLevelOutput
        fields = (
            'id',
            'title',
            'cp_output'
        )

class PMPPDResultLinkSerializer(serializers.ModelSerializer):
    result_link = serializers.CharField(source='external_id')
    id = serializers.CharField(source='external_cp_output_id')
    programme_document = serializers.PrimaryKeyRelatedField(queryset=ProgrammeDocument.objects.all())

    class Meta:
        model = PDResultLink
        fields = (
            'id',
            'title',
            'result_link',
            'programme_document'
        )

