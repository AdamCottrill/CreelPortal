import django_filters

from ...models import FN023
from .filter_utils import NumberInFilter, ValueInFilter


class FN023SubFilter(django_filters.FilterSet):
    """A fitlerset that allows us to select subsets of net set objects by
    net set attributes."""

    dtp = ValueInFilter(field_name="dtp")
    dtp__not = ValueInFilter(field_name="dtp", exclude=True)
    dtp_nm__like = django_filters.CharFilter(
        field_name="dtp_nm", lookup_expr="icontains"
    )
    dtp_nm__not_like = django_filters.CharFilter(
        field_name="dtp_nm", lookup_expr="icontains", exclude=True
    )

    class Meta:
        model = FN023
        fields = [
            "dtp",
            "dtp_nm",
        ]


class FN023Filter(FN023SubFilter):
    """Extends the FN023SubFilter to include additional fields that
    are associated with parent objects.
    """

    # FN011 ATTRIBUTES
    year = django_filters.CharFilter(
        field_name="season__creel__year", lookup_expr="exact"
    )
    year__gte = django_filters.NumberFilter(
        field_name="season__creel__year", lookup_expr="gte"
    )
    year__lte = django_filters.NumberFilter(
        field_name="season__creel__year", lookup_expr="lte"
    )

    year__gt = django_filters.NumberFilter(
        field_name="season__creel__year", lookup_expr="gt"
    )
    year__lt = django_filters.NumberFilter(
        field_name="season__creel__year", lookup_expr="lt"
    )

    prj_date0 = django_filters.DateFilter(
        field_name="season__creel__prj_date0", help_text="format: yyyy-mm-dd"
    )
    prj_date0__gte = django_filters.DateFilter(
        field_name="season__creel__prj_date0",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    prj_date0__lte = django_filters.DateFilter(
        field_name="season__creel__prj_date0",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )

    prj_date1 = django_filters.DateFilter(
        field_name="season__creel__prj_date1", help_text="format: yyyy-mm-dd"
    )
    prj_date1__gte = django_filters.DateFilter(
        field_name="season__creel__prj_date1",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    prj_date1__lte = django_filters.DateFilter(
        field_name="season__creel__prj_date1",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )

    prj_cd = ValueInFilter(field_name="season__creel__prj_cd")
    prj_cd__not = ValueInFilter(field_name="season__creel__prj_cd", exclude=True)

    prj_cd__like = django_filters.CharFilter(
        field_name="season__creel__prj_cd", lookup_expr="icontains"
    )

    prj_cd__not_like = django_filters.CharFilter(
        field_name="season__creel__prj_cd", lookup_expr="icontains", exclude=True
    )

    prj_cd__endswith = django_filters.CharFilter(
        field_name="season__creel__prj_cd", lookup_expr="endswith"
    )
    prj_cd__not_endswith = django_filters.CharFilter(
        field_name="season__creel__prj_cd", lookup_expr="endswith", exclude=True
    )

    prj_nm__like = django_filters.CharFilter(
        field_name="season__creel__prj_nm", lookup_expr="icontains"
    )

    prj_nm__not_like = django_filters.CharFilter(
        field_name="season__creel__prj_nm", lookup_expr="icontains", exclude=True
    )

    prj_ldr = django_filters.CharFilter(
        field_name="season__creel__prj_ldr__username", lookup_expr="iexact"
    )

    contmeth = ValueInFilter(field_name="season__creel__contmeth")
    contmeth__not = ValueInFilter(field_name="season__creel__contmeth", exclude=True)

    lake = ValueInFilter(field_name="season__creel__lake__abbrev")

    lake__not = ValueInFilter(field_name="season__creel__lake__abbrev", exclude=True)

    ssn_date0 = django_filters.DateFilter(
        field_name="season__ssn_date0", help_text="format: yyyy-mm-dd"
    )
    ssn_date0__gte = django_filters.DateFilter(
        field_name="season__ssn_date0",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    ssn_date0__lte = django_filters.DateFilter(
        field_name="season__ssn_date0",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )

    ssn_date1 = django_filters.DateFilter(
        field_name="season__ssn_date1", help_text="format: yyyy-mm-dd"
    )
    ssn_date1__gte = django_filters.DateFilter(
        field_name="season__ssn_date1",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    ssn_date1__lte = django_filters.DateFilter(
        field_name="season__ssn_date1",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )

    ssn = ValueInFilter(field_name="season__ssn")
    ssn__not = ValueInFilter(field_name="season__ssn", exclude=True)

    ssn__like = django_filters.CharFilter(
        field_name="season__ssn", lookup_expr="icontains"
    )

    ssn__not_like = django_filters.CharFilter(
        field_name="season__ssn", lookup_expr="icontains", exclude=True
    )

    ssn_des = ValueInFilter(field_name="season__ssn_des")
    ssn_des__not = ValueInFilter(field_name="season__ssn_des", exclude=True)

    ssn_des__like = django_filters.CharFilter(
        field_name="season__ssn_des", lookup_expr="icontains"
    )

    ssn_des__not_like = django_filters.CharFilter(
        field_name="season__ssn_des", lookup_expr="icontains", exclude=True
    )

    class Meta:
        model = FN023
        fields = [
            "season__creel__year",
            "season__creel__prj_cd",
            "season__creel__lake",
            "season__creel__contmeth",
            "season__ssn",
            "season__ssn_des",
            "season__ssn_date0",
            "season__ssn_date1",
            "dtp",
            "dtp_nm",
        ]
