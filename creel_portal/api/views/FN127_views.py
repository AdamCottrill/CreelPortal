from django.db.models import F
from rest_framework import generics

from ...models import FN127
from ..filters import FN127Filter
from ..serializers import FN127ListSerializer
from ..permissions import ReadOnly
from ..pagination import StandardResultsSetPagination


class FN127ListView(generics.ListAPIView):
    """A readonly enpoint to return FN127 - season strata data in format
    that closely matches FN-portal and FN-2 schema.."""

    serializer_class = FN127ListSerializer
    filterset_class = FN127Filter
    pagination_class = StandardResultsSetPagination
    permission_classes = [ReadOnly]

    def get_queryset(self):
        """"""
        return (
            FN127.objects.select_related(
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
                "ageid",
                "agemt",
                "agea",
                "preferred",
                "conf",
                "nca",
                "edge",
                "agest",
                "comment7",
                "id",
                "slug",
            )
        )
