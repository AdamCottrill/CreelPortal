from django.db.models import F
from rest_framework import generics

from ...models import FN124
from ..filters import FN124Filter
from ..serializers import FN124ListSerializer
from ..permissions import ReadOnly
from ..pagination import LargeResultsSetPagination


class FN124ListView(generics.ListAPIView):
    """A readonly enpoint to return FN124."""

    serializer_class = FN124ListSerializer
    filterset_class = FN124Filter
    pagination_class = LargeResultsSetPagination
    permission_classes = [ReadOnly]

    def get_queryset(self):
        """"""
        return (
            FN124.objects.select_related(
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
            )
            .order_by("slug")
            .values(
                "prj_cd",
                "sam",
                "spc",
                "grp",
                "siz",
                "sizcnt",
                "slug",
                "id",
            )
        )
