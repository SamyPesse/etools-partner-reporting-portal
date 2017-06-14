from django.db.models import Q
import django_filters
from django_filters.filters import CharFilter

from .models import ClusterObjective


class ClusterObjectiveFilter(django_filters.FilterSet):
    ref_title = CharFilter(method='get_reference_number_title')

    class Meta:
        model = ClusterObjective
        fields = ['ref_title', ]

    def get_reference_number_title(self, queryset, name, value):
        return queryset.filter(
            Q(reference_number__icontains=value) | Q(title__icontains=value)
        )
