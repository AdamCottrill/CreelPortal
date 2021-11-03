from django.db.models import F
from rest_framework import generics

from ...models import FN111
from ..filters import FN111Filter
from ..serializers import FN111Serializer, FN111ListSerializer
from ..permissions import IsPrjLeadOrAdminOrReadOnly, ReadOnly
from ..pagination import StandardResultsSetPagination


class InterviewLogList(generics.ListAPIView):
    """an api end point to list all of the creel logs (FN111) associated with a
    creel."""

    serializer_class = FN111Serializer
    filter_class = FN111Filter

    def get_queryset(self):
        """ """

        prj_cd = self.kwargs.get("prj_cd")
        return (
            FN111.objects.filter(creel__slug=prj_cd.lower())
            .prefetch_related("activity_counts")
            .select_related(
                "season", "season__creel", "period", "daytype", "area", "mode"
            )
        )


class ActivityCountList(generics.ListAPIView):
    """an api end point to list all of the activity Counts (Fn112)
    associated with an interview log (FN111) associated with a
    creel.

    These might be better as nested elements of the inteview logs.

    """

    serializer_class = FN111Serializer

    def get_queryset(self):
        """ """

        prj_cd = self.kwargs.get("prj_cd")
        sama = self.kwargs.get("sama")

        return FN112.objects.filter(sama__creel__slug=prj_cd.lower(), sama__sama=sama)


class FN111ListView(generics.ListAPIView):
    """A readonly enpoint to return FN111 - season strata data in format
    that closely matches FN-portal and FN-2 schema.."""

    serializer_class = FN111ListSerializer
    filterset_class = FN111Filter
    pagination_class = StandardResultsSetPagination
    permission_classes = [ReadOnly]

    def get_queryset(self):
        """"""
        return (
            FN111.objects.select_related(
                "creel",
                "area",
                "mode",
                "season",
                "daytype",
                "period",
            )
            .annotate(
                prj_cd=F("creel__prj_cd"),
                ssn=F("season__ssn"),
                dtp=F("daytype__dtp"),
                prd=F("period__prd"),
                space=F("area__space"),
                _mode=F("mode__mode"),
            )
            .order_by("slug")
            .values(
                "prj_cd",
                "sama",
                "ssn",
                "dtp",
                "prd",
                "space",
                "_mode",
                "date",
                "samtm0",
                "weather",
                "comment1",
                "slug",
                "id",
            )
        )
