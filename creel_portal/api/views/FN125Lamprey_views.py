from django.db.models import F
from rest_framework import generics

from ...models import FN125_Lamprey
from ..filters import FN125LampreyFilter
from ..serializers import FN125LampreyListSerializer
from ..permissions import ReadOnly
from ..pagination import StandardResultsSetPagination


class FN125LampreyListView(generics.ListAPIView):
    """A readonly enpoint to return FN125Lamprey - season strata data in format
    that closely matches FN-portal and FN-2 schema.."""

    serializer_class = FN125LampreyListSerializer
    filterset_class = FN125LampreyFilter
    pagination_class = StandardResultsSetPagination
    permission_classes = [ReadOnly]

    def get_queryset(self):
        """"""
        return (
            FN125_Lamprey.objects.select_related(
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
                "lamid",
                "xlam",
                "lamijc",
                "lamijc_type",
                "lamijc_size",
                "comment_lam",
                "slug",
                "id",
            )
        )
