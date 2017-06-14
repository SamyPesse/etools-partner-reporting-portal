from __future__ import unicode_literals

from django.contrib.postgres.fields import JSONField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from model_utils.models import TimeStampedModel

from core.common import (
    INDICATOR_REPORT_STATUS, FREQUENCY_LEVEL,
    PROGRESS_REPORT_STATUS
)


class IndicatorBlueprint(TimeStampedModel):
    """
    IndicatorBlueprint module is a pattern for indicator (here we setup basic parameter).
    """
    NUMBER = u'number'
    PERCENTAGE = u'percentage'
    YESNO = u'yesno'
    UNIT_CHOICES = (
        (NUMBER, NUMBER),
        (PERCENTAGE, PERCENTAGE),
        (YESNO, YESNO)
    )

    title = models.CharField(max_length=1024)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default=NUMBER)
    description = models.CharField(max_length=3072, null=True, blank=True)
    code = models.CharField(max_length=50, null=True, blank=True, unique=True)
    subdomain = models.CharField(max_length=255, null=True, blank=True)
    disaggregatable = models.BooleanField(default=False)

    # TODO: add:
    # siblings (similar inidcators to this indicator)
    # other_representation (exact copies with different names for some random reason)
    # children (indicators that aggregate up to this or contribute to this indicator through a formula)
    # aggregation_types (potential aggregation types: geographic, time-periods ?)
    # calculation_formula (how the children totals add up to this indicator's total value)
    # aggregation_formulas (how the total value is aggregated from the reports if possible)

    def save(self, *args, **kwargs):
        # Prevent from saving empty strings as code because of the unique together constraint
        if self.code == '':
            self.code = None
        super(IndicatorBlueprint, self).save(*args, **kwargs)


class Reportable(TimeStampedModel):
    """
    Reportable / Applied Indicator model.

    related models:
        ContentType (ForeignKey): "content_type"
        content_type & object_id fields (GenericForeignKey): "content_object"
        partner.PartnerProject (ForeignKey): "project"
        indicator.IndicatorBlueprint (ForeignKey): "blueprint"
        cluster.ClusterObjective (ForeignKey): "content_object"
        self (ForeignKey): "parent_indicator"
    """
    target = models.CharField(max_length=255, null=True, blank=True)
    baseline = models.CharField(max_length=255, null=True, blank=True)
    assumptions = models.TextField(null=True, blank=True)
    means_of_verification = models.CharField(max_length=255, null=True, blank=True)
    is_cluster_indicator = models.BooleanField(default=False)

    # Current total, transactional and dynamically calculated based on IndicatorReports
    total = models.IntegerField(null=True, blank=True, default=0,
                                verbose_name="Current Total")

    # unique code for this indicator within the current context
    # eg: (1.1) result code 1 - indicator code 1
    context_code = models.CharField(max_length=50, null=True, blank=True,
                                    verbose_name="Code in current context")

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    blueprint = models.ForeignKey(IndicatorBlueprint, null=True, related_name="reportables")
    parent_indicator = models.ForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    @property
    def ref_num(self):
        from unicef.models import LowerLevelOutput

        if isinstance(self.content_object, LowerLevelOutput):
            return self.content_object.indicator.programme_document.reference_number
        else:
            return ''

    @property
    def achieved(self):
        if self.indicator_reports.exists():
            return self.indicator_reports.last().total
        else:
            return None

    @property
    def progress_percentage(self):
        # if self.blueprint.unit == IndicatorBlueprint.NUMBER:
            # pass
        percentage = 0.0

        if self.achieved:
            percentage = (self.achieved - float(self.baseline)) / (float(self.target) - float(self.baseline))

        return percentage

    def __str__(self):
        return "Reportable <pk:%s>" % self.id


class IndicatorReport(TimeStampedModel):
    """
    IndicatorReport module is a result of partner staff activity (what they done in defined frequency scope).

    related models:
        indicator.Reportable (ForeignKey): "indicator"
        unicef.ProgressReport (ForeignKey): "progress_report"
        core.Location (OneToOneField): "location"
    """
    title = models.CharField(max_length=255)
    reportable = models.ForeignKey(Reportable, related_name="indicator_reports")
    progress_report = models.ForeignKey('unicef.ProgressReport', related_name="indicator_reports", null=True)
    time_period_start = models.DateField(auto_now=True)  # first day of defined frequency mode
    time_period_end = models.DateField()  # last day of defined frequency mode
    due_date = models.DateField()  # can be few days/weeks out of the "end date"
    submission_date = models.DateField(null=True, blank=True, verbose_name="Date of submission")
    frequency = models.CharField(
        max_length=3,
        choices=FREQUENCY_LEVEL,
        default=FREQUENCY_LEVEL.monthly,
        verbose_name='Frequency of reporting'
    )

    total = models.PositiveIntegerField(blank=True, null=True)

    remarks = models.TextField(blank=True, null=True)
    report_status = models.CharField(
        choices=INDICATOR_REPORT_STATUS,
        default=INDICATOR_REPORT_STATUS.ontrack,
        max_length=3
    )

    def __str__(self):
        return self.title

    @property
    def is_draft(self):
        if self.submission_date is None and IndicatorLocationData.objects.filter(indicator_report=self).exists():
            return True
        return False

    @property
    def progress_report_status(self):
        if self.progress_report:
            return self.progress_report.get_status_display()
        else:
            return PROGRESS_REPORT_STATUS.due

    @property
    def status(self):
        # TODO: Check all disaggregation data across locations and return status
        return 'fulfilled'


class IndicatorLocationData(TimeStampedModel):
    """
    IndicatorLocationData module it includes indicators for chosen location.

    related models:
        indicator.IndicatorReport (ForeignKey): "indicator_report"
        core.Location (OneToOneField): "location"
    """
    indicator_report = models.ForeignKey(IndicatorReport, related_name="indicator_location_data")
    location = models.ForeignKey('core.Location', related_name="indicator_location_data")

    disaggregation = JSONField(default=dict)

    def __unicode__(self):
        return "{} Location Data for {}".format(self.location, self.indicator_report)


class Disaggregation(TimeStampedModel):
    """
    Disaggregation module. For example: <Gender, Age>

    related models:
        indicator.Reportable (ForeignKey): "reportable"
    """
    name = models.CharField(max_length=255, verbose_name="Disaggregation by", null=True, blank=True)
    reportable = models.ForeignKey(Reportable, related_name="disaggregation")
    active = models.BooleanField(default=False)

    class Meta:
        unique_together = ('name', 'reportable')

    def __str__(self):
        return "Disaggregation <pk:%s>" % self.id


class DisaggregationValue(TimeStampedModel):
    """
    Disaggregation Value module. For example: Gender <Male, Female, Other>

    related models:
        indicator.Disaggregation (ForeignKey): "disaggregation"
    """
    disaggregation = models.ForeignKey(Disaggregation, related_name="disaggregation_value")
    value = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return "Disaggregation Value <pk:%s>" % self.id
