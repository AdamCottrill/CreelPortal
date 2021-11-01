import django_filters

from .filter_utils import ValueInFilter


class FishAttrFilters(django_filters.FilterSet):
    """A filter set that contains filters that are common to all the FN125 child
    tables - FN125Lamprey, FN125Tag, Fn126, and FN127.  Filtersets for those class
    inherit from this one, and add their own models and model specific filters.

    Filters in this class include filters from FN011 to FN125 Tables,
    plus those associated with the design tables.
    """

    tlen = django_filters.NumberFilter(
        field_name="fish__tlen"
    )  # , lookup_expr="exact")
    tlen__gte = django_filters.NumberFilter(field_name="fish__tlen", lookup_expr="gte")
    tlen__lte = django_filters.NumberFilter(field_name="fish__tlen", lookup_expr="lte")
    tlen__gt = django_filters.NumberFilter(field_name="fish__tlen", lookup_expr="gt")
    tlen__lt = django_filters.NumberFilter(field_name="fish__tlen", lookup_expr="lt")

    flen = django_filters.NumberFilter(field_name="fish__flen")
    flen__gte = django_filters.NumberFilter(field_name="fish__flen", lookup_expr="gte")
    flen__lte = django_filters.NumberFilter(field_name="fish__flen", lookup_expr="lte")
    flen__gt = django_filters.NumberFilter(field_name="fish__flen", lookup_expr="gt")
    flen__lt = django_filters.NumberFilter(field_name="fish__flen", lookup_expr="lt")

    rwt = django_filters.NumberFilter(field_name="fish__rwt")
    rwt__null = django_filters.BooleanFilter(
        field_name="fish__rwt", lookup_expr="isnull"
    )
    rwt__gte = django_filters.NumberFilter(field_name="fish__rwt", lookup_expr="gte")
    rwt__lte = django_filters.NumberFilter(field_name="fish__rwt", lookup_expr="lte")
    rwt__gt = django_filters.NumberFilter(field_name="fish__rwt", lookup_expr="gt")
    rwt__lt = django_filters.NumberFilter(field_name="fish__rwt", lookup_expr="lt")

    mat = ValueInFilter(field_name="fish__mat")
    mat__not = ValueInFilter(field_name="fish__mat", exclude=True)
    mat__null = django_filters.BooleanFilter(
        field_name="fish__mat", lookup_expr="isnull"
    )

    gon = ValueInFilter(field_name="fish__gon")
    gon__not = ValueInFilter(field_name="fish__gon", exclude=True)
    gon__null = django_filters.BooleanFilter(
        field_name="fish__gon", lookup_expr="isnull"
    )

    sex = ValueInFilter(field_name="fish__sex")
    sex__not = ValueInFilter(field_name="fish__sex", exclude=True)
    sex__null = django_filters.BooleanFilter(
        field_name="fish__sex", lookup_expr="isnull"
    )

    clipc = ValueInFilter(field_name="fish__clipc")
    clipc__not = ValueInFilter(field_name="fish__clipc", exclude=True)
    clipc__null = django_filters.BooleanFilter(
        field_name="fish__clipc", lookup_expr="isnull"
    )
    clipc__like = django_filters.CharFilter(
        field_name="fish__clipc", lookup_expr="icontains"
    )
    clipc__not_like = django_filters.CharFilter(
        field_name="fish__clipc", lookup_expr="icontains", exclude=True
    )

    fate = ValueInFilter(field_name="fish__fate")
    fate__not = ValueInFilter(field_name="fish__fate", exclude=True)
    fate__null = django_filters.BooleanFilter(
        field_name="fish__fate", lookup_expr="isnull"
    )

    agest__like = django_filters.CharFilter(
        field_name="fish__agest", lookup_expr="icontains"
    )

    # CATCH ATTRIBUTES

    spc = ValueInFilter(field_name="fish__catch__species__spc")
    spc__not = ValueInFilter(field_name="fish__catch__species__spc", exclude=True)

    grp = ValueInFilter(field_name="fish__catch__grp")
    grp__not = ValueInFilter(field_name="fish__catch__grp", exclude=True)

    sek = django_filters.BooleanFilter(field_name="fish__catch__sek")

    hsvcnt = django_filters.CharFilter(
        field_name="fish__catch__hsvcnt", lookup_expr="exact"
    )
    hsvcnt__gte = django_filters.NumberFilter(
        field_name="fish__catch__hsvcnt", lookup_expr="gte"
    )
    hsvcnt__lte = django_filters.NumberFilter(
        field_name="fish__catch__hsvcnt", lookup_expr="lte"
    )
    hsvcnt__gt = django_filters.NumberFilter(
        field_name="fish__catch__hsvcnt", lookup_expr="gt"
    )
    hsvcnt__lt = django_filters.NumberFilter(
        field_name="fish__catch__hsvcnt", lookup_expr="lt"
    )

    rlscnt = django_filters.CharFilter(
        field_name="fish__catch__rlscnt", lookup_expr="exact"
    )
    rlscnt__gte = django_filters.NumberFilter(
        field_name="fish__catch__rlscnt", lookup_expr="gte"
    )
    rlscnt__lte = django_filters.NumberFilter(
        field_name="fish__catch__rlscnt", lookup_expr="lte"
    )
    rlscnt__gt = django_filters.NumberFilter(
        field_name="fish__catch__rlscnt", lookup_expr="gt"
    )
    rlscnt__lt = django_filters.NumberFilter(
        field_name="fish__catch__rlscnt", lookup_expr="lt"
    )

    mescnt = django_filters.CharFilter(
        field_name="fish__catch__mescnt", lookup_expr="exact"
    )
    mescnt__gte = django_filters.NumberFilter(
        field_name="fish__catch__mescnt", lookup_expr="gte"
    )
    mescnt__lte = django_filters.NumberFilter(
        field_name="fish__catch__mescnt", lookup_expr="lte"
    )
    mescnt__gt = django_filters.NumberFilter(
        field_name="fish__catch__mescnt", lookup_expr="gt"
    )
    mescnt__lt = django_filters.NumberFilter(
        field_name="fish__catch__mescnt", lookup_expr="lt"
    )

    # INTERVIEW ATTRIBUTES:

    itvtm0 = django_filters.TimeFilter(
        field_name="fish__catch__interview__itvtm0", help_text="format: HH:MM"
    )
    itvtm0__gte = django_filters.TimeFilter(
        field_name="fish__catch__interview__itvtm0",
        lookup_expr="gte",
        help_text="format: HH:MM",
    )
    itvtm0__lte = django_filters.TimeFilter(
        field_name="fish__catch__interview__itvtm0",
        lookup_expr="lte",
        help_text="format: HH:MM",
    )
    itvtm0__gt = django_filters.TimeFilter(
        field_name="fish__catch__interview__itvtm0",
        lookup_expr="gt",
        help_text="format: HH:MM",
    )
    itvtm0__lt = django_filters.TimeFilter(
        field_name="fish__catch__interview__itvtm0",
        lookup_expr="lt",
        help_text="format: HH:MM",
    )

    efftm0 = django_filters.TimeFilter(
        field_name="fish__catch__interview__efftm0", help_text="format: HH:MM"
    )
    efftm0__gte = django_filters.TimeFilter(
        field_name="fish__catch__interview__efftm0",
        lookup_expr="gte",
        help_text="format: HH:MM",
    )
    efftm0__lte = django_filters.TimeFilter(
        field_name="fish__catch__interview__efftm0",
        lookup_expr="lte",
        help_text="format: HH:MM",
    )
    efftm0__gt = django_filters.TimeFilter(
        field_name="fish__catch__interview__efftm0",
        lookup_expr="gt",
        help_text="format: HH:MM",
    )
    efftm0__lt = django_filters.TimeFilter(
        field_name="fish__catch__interview__efftm0",
        lookup_expr="lt",
        help_text="format: HH:MM",
    )

    efftm1 = django_filters.TimeFilter(
        field_name="fish__catch__interview__efftm1", help_text="format: HH:MM"
    )
    efftm1__gte = django_filters.TimeFilter(
        field_name="fish__catch__interview__efftm1",
        lookup_expr="gte",
        help_text="format: HH:MM",
    )
    efftm1__lte = django_filters.TimeFilter(
        field_name="fish__catch__interview__efftm1",
        lookup_expr="lte",
        help_text="format: HH:MM",
    )
    efftm1__gt = django_filters.TimeFilter(
        field_name="fish__catch__interview__efftm1",
        lookup_expr="gt",
        help_text="format: HH:MM",
    )
    efftm1__lt = django_filters.TimeFilter(
        field_name="fish__catch__interview__efftm1",
        lookup_expr="lt",
        help_text="format: HH:MM",
    )

    date = django_filters.DateFilter(
        field_name="fish__catch__interview__date", help_text="format: yyyy-mm-dd"
    )
    date__gte = django_filters.DateFilter(
        field_name="fish__catch__interview__date",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    date__lte = django_filters.DateFilter(
        field_name="fish__catch__interview__date",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )
    date__gt = django_filters.DateFilter(
        field_name="fish__catch__interview__date",
        lookup_expr="gt",
        help_text="format: yyyy-mm-dd",
    )
    date__lt = django_filters.DateFilter(
        field_name="fish__catch__interview__date",
        lookup_expr="lt",
        help_text="format: yyyy-mm-dd",
    )

    persons = django_filters.CharFilter(
        field_name="fish__catch__interview__persons", lookup_expr="exact"
    )
    persons__gte = django_filters.NumberFilter(
        field_name="fish__catch__interview__persons", lookup_expr="gte"
    )
    persons__lte = django_filters.NumberFilter(
        field_name="fish__catch__interview__persons", lookup_expr="lte"
    )
    persons__gt = django_filters.NumberFilter(
        field_name="fish__catch__interview__persons", lookup_expr="gt"
    )
    persons__lt = django_filters.NumberFilter(
        field_name="fish__catch__interview__persons", lookup_expr="lt"
    )

    anglers = django_filters.CharFilter(
        field_name="fish__catch__interview__anglers", lookup_expr="exact"
    )
    anglers__gte = django_filters.NumberFilter(
        field_name="fish__catch__interview__anglers", lookup_expr="gte"
    )
    anglers__lte = django_filters.NumberFilter(
        field_name="fish__catch__interview__anglers", lookup_expr="lte"
    )
    anglers__gt = django_filters.NumberFilter(
        field_name="fish__catch__interview__anglers", lookup_expr="gt"
    )
    anglers__lt = django_filters.NumberFilter(
        field_name="fish__catch__interview__anglers", lookup_expr="lt"
    )

    rods = django_filters.CharFilter(
        field_name="fish__catch__interview__rods", lookup_expr="exact"
    )
    rods__gte = django_filters.NumberFilter(
        field_name="fish__catch__interview__rods", lookup_expr="gte"
    )
    rods__lte = django_filters.NumberFilter(
        field_name="fish__catch__interview__rods", lookup_expr="lte"
    )
    rods__gt = django_filters.NumberFilter(
        field_name="fish__catch__interview__rods", lookup_expr="gt"
    )
    rods__lt = django_filters.NumberFilter(
        field_name="fish__catch__interview__rods", lookup_expr="lt"
    )

    angmeth = ValueInFilter(field_name="fish__catch__interview__angmeth")
    angmeth__not = ValueInFilter(
        field_name="fish__catch__interview__angmeth", exclude=True
    )

    comment1__like = django_filters.CharFilter(
        field_name="fish__catch__interview__comment1", lookup_expr="icontains"
    )

    # FN011 ATTRIBUTES
    year = django_filters.CharFilter(
        field_name="fish__catch__interview__sama__creel__year", lookup_expr="exact"
    )
    year__gte = django_filters.NumberFilter(
        field_name="fish__catch__interview__sama__creel__year", lookup_expr="gte"
    )
    year__lte = django_filters.NumberFilter(
        field_name="fish__catch__interview__sama__creel__year", lookup_expr="lte"
    )

    year__gt = django_filters.NumberFilter(
        field_name="fish__catch__interview__sama__creel__year", lookup_expr="gt"
    )
    year__lt = django_filters.NumberFilter(
        field_name="fish__catch__interview__sama__creel__year", lookup_expr="lt"
    )

    prj_date0 = django_filters.DateFilter(
        field_name="fish__catch__interview__sama__creel__prj_date0",
        help_text="format: yyyy-mm-dd",
    )
    prj_date0__gte = django_filters.DateFilter(
        field_name="fish__catch__interview__sama__creel__prj_date0",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    prj_date0__lte = django_filters.DateFilter(
        field_name="fish__catch__interview__sama__creel__prj_date0",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )

    prj_date1 = django_filters.DateFilter(
        field_name="fish__catch__interview__sama__creel__prj_date1",
        help_text="format: yyyy-mm-dd",
    )
    prj_date1__gte = django_filters.DateFilter(
        field_name="fish__catch__interview__sama__creel__prj_date1",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    prj_date1__lte = django_filters.DateFilter(
        field_name="fish__catch__interview__sama__creel__prj_date1",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )

    prj_cd = ValueInFilter(field_name="fish__catch__interview__sama__creel__prj_cd")
    prj_cd__not = ValueInFilter(
        field_name="fish__catch__interview__sama__creel__prj_cd", exclude=True
    )

    prj_cd__like = django_filters.CharFilter(
        field_name="fish__catch__interview__sama__creel__prj_cd",
        lookup_expr="icontains",
    )

    prj_cd__not_like = django_filters.CharFilter(
        field_name="fish__catch__interview__sama__creel__prj_cd",
        lookup_expr="icontains",
        exclude=True,
    )

    prj_cd__endswith = django_filters.CharFilter(
        field_name="fish__catch__interview__sama__creel__prj_cd", lookup_expr="endswith"
    )
    prj_cd__not_endswith = django_filters.CharFilter(
        field_name="fish__catch__interview__sama__creel__prj_cd",
        lookup_expr="endswith",
        exclude=True,
    )

    prj_nm__like = django_filters.CharFilter(
        field_name="fish__catch__interview__sama__creel__prj_nm",
        lookup_expr="icontains",
    )

    prj_nm__not_like = django_filters.CharFilter(
        field_name="fish__catch__interview__sama__creel__prj_nm",
        lookup_expr="icontains",
        exclude=True,
    )

    prj_ldr = django_filters.CharFilter(
        field_name="fish__catch__interview__sama__creel__prj_ldr__username",
        lookup_expr="iexact",
    )

    contmeth = ValueInFilter(field_name="fish__catch__interview__sama__creel__contmeth")
    contmeth__not = ValueInFilter(
        field_name="fish__catch__interview__sama__creel__contmeth", exclude=True
    )

    lake = ValueInFilter(field_name="fish__catch__interview__sama__creel__lake__abbrev")

    lake__not = ValueInFilter(
        field_name="fish__catch__interview__sama__creel__lake__abbrev", exclude=True
    )

    # SEASON FILTERS:
    ssn = ValueInFilter(field_name="fish__catch__interview__sama__season__ssn")
    ssn__not = ValueInFilter(
        field_name="fish__catch__interview__sama__season__ssn", exclude=True
    )

    ssn__like = django_filters.CharFilter(
        field_name="fish__catch__interview__sama__season__ssn", lookup_expr="icontains"
    )

    ssn__not_like = django_filters.CharFilter(
        field_name="fish__catch__interview__sama__season__ssn",
        lookup_expr="icontains",
        exclude=True,
    )

    ssn_des = ValueInFilter(field_name="fish__catch__interview__sama__season__ssn_des")
    ssn_des__not = ValueInFilter(
        field_name="fish__catch__interview__sama__season__ssn_des", exclude=True
    )

    ssn_des__like = django_filters.CharFilter(
        field_name="fish__catch__interview__sama__season__ssn_des",
        lookup_expr="icontains",
    )

    ssn_des__not_like = django_filters.CharFilter(
        field_name="fish__catch__interview__sama__season__ssn_des",
        lookup_expr="icontains",
        exclude=True,
    )

    ssn_date0 = django_filters.DateFilter(
        field_name="fish__catch__interview__sama__season__ssn_date0",
        help_text="format: yyyy-mm-dd",
    )
    ssn_date0__gte = django_filters.DateFilter(
        field_name="fish__catch__interview__sama__season__ssn_date0",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    ssn_date0__lte = django_filters.DateFilter(
        field_name="fish__catch__interview__sama__season__ssn_date0",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )

    ssn_date1 = django_filters.DateFilter(
        field_name="fish__catch__interview__sama__season__ssn_date1",
        help_text="format: yyyy-mm-dd",
    )
    ssn_date1__gte = django_filters.DateFilter(
        field_name="fish__catch__interview__sama__season__ssn_date1",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    ssn_date1__lte = django_filters.DateFilter(
        field_name="fish__catch__interview__sama__season__ssn_date1",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )

    # daytype filters
    dtp = ValueInFilter(field_name="fish__catch__interview__sama__daytype__dtp")
    dtp__not = ValueInFilter(
        field_name="fish__catch__interview__sama__daytype__dtp", exclude=True
    )
    dtp_nm__like = django_filters.CharFilter(
        field_name="fish__catch__interview__sama__daytype__dtp_nm",
        lookup_expr="icontains",
    )
    dtp_nm__not_like = django_filters.CharFilter(
        field_name="fish__catch__interview__sama__daytype__dtp_nm",
        lookup_expr="icontains",
        exclude=True,
    )

    # Period filters
    prd = ValueInFilter(field_name="fish__catch__interview__sama__prd__prd")
    prd__not = ValueInFilter(
        field_name="fish__catch__interview__sama__prd__prd", exclude=True
    )

    prdtm0 = django_filters.TimeFilter(
        field_name="fish__catch__interview__sama__prd__prdtm0",
        help_text="format: HH:MM",
    )
    prdtm0__gte = django_filters.TimeFilter(
        field_name="fish__catch__interview__sama__prd__prdtm0",
        lookup_expr="gte",
        help_text="format: HH:MM",
    )
    prdtm0__lte = django_filters.TimeFilter(
        field_name="fish__catch__interview__sama__prd__prdtm0",
        lookup_expr="lte",
        help_text="format: HH:MM",
    )

    prdtm1 = django_filters.TimeFilter(
        field_name="fish__catch__interview__sama__prd__prdtm1",
        help_text="format: HH:MM",
    )
    prdtm1__gte = django_filters.TimeFilter(
        field_name="fish__catch__interview__sama__prd__prdtm1",
        lookup_expr="gte",
        help_text="format: HH:MM",
    )
    prdtm1__lte = django_filters.TimeFilter(
        field_name="fish__catch__interview__sama__prd__prdtm1",
        lookup_expr="lte",
        help_text="format: HH:MM",
    )

    prd_dur__gte = django_filters.NumberFilter(
        field_name="fish__catch__interview__sama__prd__prd_dur", lookup_expr="gte"
    )
    prd_dur__lte = django_filters.NumberFilter(
        field_name="fish__catch__interview__sama__prd__prd_dur", lookup_expr="lte"
    )

    # SPACE filters
    space = ValueInFilter(field_name="fish__catch__interview__sama__area__space")
    space__not = ValueInFilter(
        field_name="fish__catch__interview__sama__area__space", exclude=True
    )

    space__like = django_filters.CharFilter(
        field_name="fish__catch__interview__sama__area__space", lookup_expr="icontains"
    )

    space__not_like = django_filters.CharFilter(
        field_name="fish__catch__interview__sama__area__space",
        lookup_expr="icontains",
        exclude=True,
    )

    space_des = ValueInFilter(
        field_name="fish__catch__interview__sama__area__space_des"
    )
    space_des__not = ValueInFilter(
        field_name="fish__catch__interview__sama__area__space_des", exclude=True
    )

    space_des__like = django_filters.CharFilter(
        field_name="fish__catch__interview__sama__area__space_des",
        lookup_expr="icontains",
    )

    space_des__not_like = django_filters.CharFilter(
        field_name="fish__catch__interview__sama__area__space_des",
        lookup_expr="icontains",
        exclude=True,
    )

    # TO DO - add NULL NOT_NULL
    space_siz__gte = django_filters.NumberFilter(
        field_name="fish__catch__interview__sama__area__space_siz", lookup_expr="gte"
    )
    space_siz__lte = django_filters.NumberFilter(
        field_name="fish__catch__interview__sama__area__space_siz", lookup_expr="lte"
    )
    space_siz__gt = django_filters.NumberFilter(
        field_name="fish__catch__interview__sama__area__space_siz", lookup_expr="gt"
    )
    space_siz__lt = django_filters.NumberFilter(
        field_name="fish__catch__interview__sama__area__space_siz", lookup_expr="lt"
    )

    # TO DO - add NULL NOT_NULL
    area_cnt__gte = django_filters.NumberFilter(
        field_name="fish__catch__interview__sama__area__area_cnt", lookup_expr="gte"
    )
    area_cnt__lte = django_filters.NumberFilter(
        field_name="fish__catch__interview__sama__area__area_cnt", lookup_expr="lte"
    )
    area_cnt__gt = django_filters.NumberFilter(
        field_name="fish__catch__interview__sama__area__area_cnt", lookup_expr="gt"
    )
    area_cnt__lt = django_filters.NumberFilter(
        field_name="fish__catch__interview__sama__area__area_cnt", lookup_expr="lt"
    )

    # TO DO - add NULL NOT_NULL
    area_wt__gte = django_filters.NumberFilter(
        field_name="fish__catch__interview__sama__area__area_wt", lookup_expr="gte"
    )
    area_wt__lte = django_filters.NumberFilter(
        field_name="fish__catch__interview__sama__area__area_wt", lookup_expr="lte"
    )
    area_wt__gt = django_filters.NumberFilter(
        field_name="fish__catch__interview__sama__area__area_wt", lookup_expr="gt"
    )
    area_wt__lt = django_filters.NumberFilter(
        field_name="fish__catch__interview__sama__area__area_wt", lookup_expr="lt"
    )

    # MODE

    mode = ValueInFilter(field_name="fish__catch__interview__sama__mode__mode")
    mode__not = ValueInFilter(
        field_name="fish__catch__interview__sama__mode__mode", exclude=True
    )

    mode__like = django_filters.CharFilter(
        field_name="fish__catch__interview__sama__mode__mode", lookup_expr="icontains"
    )

    mode__not_like = django_filters.CharFilter(
        field_name="fish__catch__interview__sama__mode__mode",
        lookup_expr="icontains",
        exclude=True,
    )

    mode_des = ValueInFilter(field_name="fish__catch__interview__sama__mode__mode_des")
    mode_des__not = ValueInFilter(
        field_name="fish__catch__interview__sama__mode__mode_des", exclude=True
    )

    mode_des__like = django_filters.CharFilter(
        field_name="fish__catch__interview__sama__mode__mode_des",
        lookup_expr="icontains",
    )

    mode_des__not_like = django_filters.CharFilter(
        field_name="fish__catch__interview__sama__mode__mode_des",
        lookup_expr="icontains",
        exclude=True,
    )
