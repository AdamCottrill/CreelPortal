"""
=============================================================
~/creel_portal/creel_portal/api/filters.py
 Created: 29 Mar 2020 09:49:43


 DESCRIPTION:

  Filters associated with our api endpoints

 A. Cottrill
=============================================================
"""


from django_filters import rest_framework as filters

from ...models.fishnet2 import FN121
from .filter_utils import ValueInFilter


class FN121Filter(filters.FilterSet):
    """FN121 objects represent creel inteviews.  They will already be
    filtered by creel, so we want to be able to filter them by season,
    daytype, period, space and mode.

    """

    sama = ValueInFilter(field_name="sama__sama", lookup_expr="in")
    season = ValueInFilter(field_name="sama__season__ssn", lookup_expr="in")
    daytype = ValueInFilter(field_name="sama__daytype__dtp", lookup_expr="in")
    period = ValueInFilter(field_name="sama__period__prd", lookup_expr="in")
    area = ValueInFilter(field_name="sama__area__space", lookup_expr="in")
    mode = ValueInFilter(field_name="sama__mode__mode", lookup_expr="in")

    class Meta:
        model = FN121
        fields = ["sama", "season", "daytype", "period", "area", "mode"]
