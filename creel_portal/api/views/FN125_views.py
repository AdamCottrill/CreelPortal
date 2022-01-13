from django.db.models import F
from rest_framework import generics

from ...models import FN125
from ..filters import FN125Filter
from ..serializers import FN125Serializer, FN125ListSerializer
from ..permissions import ReadOnly
from ..pagination import LargeResultsSetPagination


class FN125ListView(generics.ListAPIView):
    """A readonly enpoint to return FN125 - season strata data in format
    that closely matches FN-portal and FN-2 schema.."""

    serializer_class = FN125ListSerializer
    filterset_class = FN125Filter
    pagination_class = LargeResultsSetPagination
    permission_classes = [ReadOnly]

    def get_queryset(self):
        """"""
        return (
            FN125.objects.select_related(
                "catch",
                "catch__interview",
                "catch__interview__sama",
                "catch__interview__sama__creel",
            )
            .annotate(
                prj_cd=F("catch__interview__sama__creel__prj_cd"),
                sam=F("catch__interview__sam"),
                spc=F("catch__species__spc"),
                grp=F("catch__grp"),
                _fish=F("fish"),
            )
            .order_by("slug")
            .values(
                "prj_cd",
                "sam",
                "spc",
                "grp",
                "_fish",
                "flen",
                "tlen",
                "rwt",
                "sex",
                "gon",
                "mat",
                "age",
                "agest",
                "clipc",
                "fate",
                "slug",
                "id",
            )
        )
