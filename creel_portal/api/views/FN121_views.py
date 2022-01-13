from django.db.models import F
from rest_framework import generics

from ...models import FN121
from ..filters import FN121Filter
from ..serializers import FN121Serializer, FN121ListSerializer
from ..permissions import ReadOnly
from ..pagination import LargeResultsSetPagination


class InterviewList(generics.ListAPIView):
    """an api end point to list all of the creel endpoints (FN121) associated with a
    creel."""

    serializer_class = FN121Serializer
    filter_class = FN121Filter

    def get_queryset(self):
        """ """

        prj_cd = self.kwargs.get("prj_cd")
        return (
            FN121.objects.filter(sama__creel__slug=prj_cd.lower())
            .prefetch_related("catch_counts", "catch_counts__species")
            .select_related(
                "sama",
                "sama__season",
                "sama__season__creel",
                "sama__period",
                "sama__daytype",
                "sama__area",
                "sama__mode",
            )
        )


class FN121ListView(generics.ListAPIView):
    """A readonly enpoint to return FN121 - season strata data in format
    that closely matches FN-portal and FN-2 schema.."""

    serializer_class = FN121ListSerializer
    filterset_class = FN121Filter
    pagination_class = LargeResultsSetPagination
    permission_classes = [ReadOnly]

    def get_queryset(self):
        """"""
        return (
            FN121.objects.select_related("sama", "sama__creel")
            .annotate(
                prj_cd=F("sama__creel__prj_cd"),
                _sama=F("sama__sama"),
                ssn=F("sama__season__ssn"),
                dtp=F("sama__daytype__dtp"),
                prd=F("sama__period__prd"),
                space=F("sama__area__space"),
                mode=F("sama__mode__mode"),
            )
            .order_by("slug")
            .values(
                "prj_cd",
                "_sama",
                "ssn",
                "dtp",
                "prd",
                "space",
                "mode",
                "sam",
                "itvseq",
                "itvtm0",
                "date",
                "efftm0",
                "efftm1",
                "effcmp",
                "effdur",
                "persons",
                "anglers",
                "rods",
                "angmeth",
                "angvis",
                "angorig",
                "angop1",
                "angop2",
                "angop3",
                "comment1",
                "slug",
                "id",
            )
        )
