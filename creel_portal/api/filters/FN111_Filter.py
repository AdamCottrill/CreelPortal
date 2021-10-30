import django_filters
from django_filters import rest_framework as filters

from ...models.creel import FN111
from .filter_utils import ValueInFilter


class FN111Filter(filters.FilterSet):
    """FN111 objects represent our creel logs.  They will already be
    filtered by creel, so we want to be able to filter them by by
    season, daytype, period, space and mode.

    """

    season = ValueInFilter(field_name="season__ssn", lookup_expr="in")
    daytype = ValueInFilter(field_name="daytype__dtp", lookup_expr="in")
    period = ValueInFilter(field_name="period__prd", lookup_expr="in")
    area = ValueInFilter(field_name="area__space", lookup_expr="in")
    mode = ValueInFilter(field_name="mode__mode", lookup_expr="in")

    class Meta:
        model = FN111
        fields = ["season", "daytype", "period", "area", "mode"]
