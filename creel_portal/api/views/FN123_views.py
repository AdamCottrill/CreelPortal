from django.db.models import F
from rest_framework import generics

from ...models import FN123
from ..filters import FN123Filter
from ..serializers import FN123Serializer, FN123ListSerializer
from ..permissions import ReadOnly
from ..pagination import LargeResultsSetPagination


class FN123ListView(generics.ListAPIView):
    """A readonly enpoint to return FN123 - season strata data in format
    that closely matches FN-portal and FN-2 schema.."""

    serializer_class = FN123ListSerializer
    filterset_class = FN123Filter
    pagination_class = LargeResultsSetPagination
    permission_classes = [ReadOnly]

    def get_queryset(self):
        """"""
        return (
            FN123.objects.select_related(
                "interview", "interview__sama", "interview__sama__creel"
            )
            .annotate(
                prj_cd=F("interview__sama__creel__prj_cd"),
                sam=F("interview__sam"),
                spc=F("species__spc"),
            )
            .order_by("slug")
            .values(
                "prj_cd",
                "sam",
                "spc",
                "grp",
                "sek",
                "hvscnt",
                "rlscnt",
                "mescnt",
                "meswt",
                "slug",
                "id",
            )
        )
