from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status as statuses
from .permissions import IsAuthenticated
from .models import Intervention, Location, ResponsePlan
from .serializers import (
    SimpleInterventionSerializer,
    ShortLocationSerializer,
    ChildrenLocationSerializer,
    ResponsePlanSerializer,
)


class SimpleInterventionAPIView(ListAPIView):
    """
    Endpoint for getting Intervention.
    Intervention need to have defined location to be displayed on drop down menu.
    """
    queryset = Intervention.objects.prefetch_related('locations').filter(locations__isnull=False).distinct()
    serializer_class = SimpleInterventionSerializer
    permission_classes = (IsAuthenticated, )


class SimpleLocationListAPIView(ListAPIView):
    """
    Endpoint for getting all Location objects.
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = ShortLocationSerializer
    lookup_field = lookup_url_kwarg = 'response_plan_id'

    def get_queryset(self):
        response_plan_id = self.kwargs.get(self.lookup_field)
        result = ResponsePlan.objects.filter(id=response_plan_id).values_list(
            'clusters__cluster_objectives__reportables__locations',
            'clusters__cluster_objectives__cluster_activities__reportables__locations',
            'clusters__partner_projects__reportables__locations',
            'clusters__partner_projects__partner_activities__reportables__locations',
        ).distinct()
        pks = []
        [pks.extend(filter(lambda x: x is not None, part)) for part in result]
        return Location.objects.filter(pk__in=pks)


class ChildrenLocationAPIView(ListAPIView):
    """
    Endpoint for fill location parameter on PD list filterset.
    """
    serializer_class = ChildrenLocationSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        # IMO we want to display via Country -> Region and/or City and/or District and/or Point
        # That should be enough.
        return Location.objects.filter(
            Q(parent_id=self.location_id) |
            Q(parent__parent_id=self.location_id) |
            Q(parent__parent__parent_id=self.location_id) |
            Q(parent__parent__parent__parent_id=self.location_id)
        )

    def list(self, request, location_id, *args, **kwargs):
        self.location_id = location_id
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            serializer.data,
            status=statuses.HTTP_200_OK
        )


class ResponsePlanAPIView(ListAPIView):
    """
    Endpoint for getting ResponsePlan.
    ResponsePlan need to have defined of intervention to be displayed on drop down menu.
    """

    serializer_class = ResponsePlanSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        intervention_id = self.kwargs.get('intervention_id')
        return ResponsePlan.objects.filter(intervention_id=intervention_id)
