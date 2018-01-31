from django.conf.urls import url

from .views import (
    ClusterListAPIView,
    ClusterObjectiveAPIView,
    ClusterObjectiveListCreateAPIView,
    ClusterActivityAPIView,
    ClusterActivityListAPIView,
    IndicatorReportsListAPIView,
    IndicatorReportsSimpleListAPIView,
    ClusterIndicatorsListExcelExportView,
    ClusterIndicatorsLocationListAPIView,
    ClusterIndicatorsListExcelExportForAnalysisView,
    ResponsePlanClusterDashboardAPIView,
    ResponsePlanPartnerDashboardAPIView,
    PartnerAnalysisSummaryAPIView,
    PartnerAnalysisIndicatorResultAPIView,
    OperationalPresenceLocationListAPIView,
    OperationalPresenceAggregationDataAPIView,
)


urlpatterns = [
    url(r'^cluster-list/(?P<response_plan_id>\d+)/$', ClusterListAPIView.as_view(),
        name="cluster-list"),
    url(r'^cluster-objective/$', ClusterObjectiveAPIView.as_view(),
        name="cluster-objective"),
    url(r'^cluster-objective/(?P<pk>\d+)/$', ClusterObjectiveAPIView.as_view(),
        name="cluster-objective"),
    url(r'^(?P<response_plan_id>\d+)/cluster-objective-list/$',
        ClusterObjectiveListCreateAPIView.as_view(),
        name="cluster-objective-list"),
    url(r'^cluster-activity/(?P<pk>\d+)/$', ClusterActivityAPIView.as_view(),
        name="cluster-activity"),
    url(r'^(?P<response_plan_id>\d+)/cluster-activity-list/$',
        ClusterActivityListAPIView.as_view(),
        name="cluster-activity-list"),
    url(r'^(?P<response_plan_id>\d+)/cluster-indicator-reports-list/$',
        IndicatorReportsListAPIView.as_view(),
        name="cluster-indicator-reports-list"),
    url(r'^(?P<response_plan_id>\d+)/cluster-indicator-reports-simple-list/$',
        IndicatorReportsSimpleListAPIView.as_view(),
        name="cluster-indicator-reports-simple-list"),
    url(r'^(?P<response_plan_id>\d+)/cluster-simple-list/$',
        ClusterListAPIView.as_view(),
        name="cluster-simple-list"),

    url(r'^(?P<response_plan_id>\d+)/cluster-dashboard/$',
        ResponsePlanClusterDashboardAPIView.as_view(),
        name="response-plan-cluster-dashboard"),
    url(r'^(?P<response_plan_id>\d+)/partner-dashboard/$',
        ResponsePlanPartnerDashboardAPIView.as_view(),
        name="response-plan-partner-dashboard"),

    url(r'^(?P<response_plan_id>\d+)/cluster-indicator-reports-list/export/$',
        ClusterIndicatorsListExcelExportView.as_view(),
        name="cluster-indicators-list-excel"),

    url(r'^(?P<response_plan_id>\d+)/cluster-indicator-reports-list/export-for-analysis/$',
        ClusterIndicatorsListExcelExportForAnalysisView.as_view(),
        name="cluster-indicators-list-excel"),

    url(r'^(?P<response_plan_id>\d+)/cluster-indicators-locations/$',
        ClusterIndicatorsLocationListAPIView.as_view(),
        name="cluster-indicators-locations"),

    url(r'^partner-analysis/$',
        PartnerAnalysisSummaryAPIView.as_view(),
        name="partner-analysis-summary"),

    url(r'^partner-analysis/response-plan/(?P<response_plan_id>\d+)/indicator/(?P<reportable_id>\d+)$',
        PartnerAnalysisIndicatorResultAPIView.as_view(),
        name="partner-analysis-indicator-result"),

    url(r'^cluster-analysis/(?P<response_plan_id>\d+)/operational-presence/map$',
        OperationalPresenceLocationListAPIView.as_view(),
        name="cluster-analysis-operational-presence-ma"),

    url(r'^cluster-analysis/(?P<response_plan_id>\d+)/operational-presence/data$',
        OperationalPresenceAggregationDataAPIView.as_view(),
        name="cluster-analysis-operational-presence-aggregation-data"),
]
