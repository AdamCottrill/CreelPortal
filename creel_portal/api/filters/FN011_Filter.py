import django_filters
from django_filters import rest_framework as filters

from ...models.fishnet2 import FN011

from .filter_utils import ValueInFilter


class FN011Filter(filters.FilterSet):
    """FN011 objects represent creel.  We want to be able to filter them
    by year, creel type, lake, and project lead."""

    lake = ValueInFilter(field_name="lake__abbrev", lookup_expr="in")

    # year will have more than one filter eventually
    # still need between, greater than and less than
    first_year = django_filters.NumberFilter(field_name="year", lookup_expr="gte")
    last_year = django_filters.NumberFilter(field_name="year", lookup_expr="lte")
    year = django_filters.CharFilter(field_name="year", lookup_expr="exact")

    class Meta:
        model = FN011
        fields = ["prj_ldr", "lake", "first_year", "last_year", "year"]
