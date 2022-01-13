from django.db.models import F
from rest_framework import generics

from ...models import FN126
from ..filters import FN126Filter
from ..serializers import FN126ListSerializer
from ..permissions import ReadOnly
from ..pagination import LargeResultsSetPagination


class FN126ListView(generics.ListAPIView):
    """A readonly enpoint to return FN126 - season strata data in format
    that closely matches FN-portal and FN-2 schema.."""

    serializer_class = FN126ListSerializer
    filterset_class = FN126Filter
    pagination_class = LargeResultsSetPagination
    permission_classes = [ReadOnly]

    def get_queryset(self):
        """"""
        return (
            FN126.objects.select_related(
                "fish",
                "fish__catch",
                "fish__catch__interview",
                "fish__catch__interview__sama",
                "fish__catch__interview__sama__creel",
            )
            .annotate(
                prj_cd=F("fish__catch__interview__sama__creel__prj_cd"),
                sam=F("fish__catch__interview__sam"),
                spc=F("fish__catch__species__spc"),
                grp=F("fish__catch__grp"),
                _fish=F("fish__fish"),
            )
            .order_by("slug")
            .values(
                "prj_cd",
                "sam",
                "spc",
                "grp",
                "_fish",
                "food",
                "taxon",
                "foodcnt",
                "comment6",
                "slug",
                "id",
            )
        )
