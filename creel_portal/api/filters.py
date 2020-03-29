"""
=============================================================
~/creel_portal/creel_portal/api/filters.py
 Created: 29 Mar 2020 09:49:43


 DESCRIPTION:

  Filters associated with our api endpoints

 A. Cottrill
=============================================================
"""

import django_filters
from django_filters import rest_framework as filters


from ..models import FN011, FN111, FN121


class ValueInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


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
