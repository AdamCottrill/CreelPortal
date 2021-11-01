from django.db.models import F
from rest_framework import generics

from ...models import FN112
from ..filters import FN112Filter
from ..serializers import FN112Serializer, FN112ListSerializer
from ..permissions import ReadOnly
from ..pagination import StandardResultsSetPagination


class FN112ListView(generics.ListAPIView):
    """A readonly enpoint to return FN112 - season strata data in format
    that closely matches FN-portal and FN-2 schema.."""

    serializer_class = FN112ListSerializer
    filterset_class = FN112Filter
    pagination_class = StandardResultsSetPagination
    permission_classes = [ReadOnly]

    def get_queryset(self):
        """"""
        return (
            FN112.objects.select_related("sama__creel", "sama")
            .annotate(
                prj_cd=F("sama__creel__prj_cd"),
                _sama=F("sama__sama"),
            )
            .order_by("slug")
            .values(
                "prj_cd",
                "_sama",
                "atytm0",
                "atytm1",
                "atycnt",
                "chkcnt",
                "itvcnt",
                "atydur",
                "slug",
                "id",
            )
        )
