import django_filters


class ValueInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass
