"""
=============================================================
 ~/creel_portal/api/views/FN022_views.py
 Created: 29 Oct 2021 14:36:23

 DESCRIPTION:



 A. Cottrill
=============================================================
"""

from django.db.models import F
from rest_framework import generics

from ...models import FN022
from ..serializers import (
    FN022Serializer,
    FN022ListSerializer,
    TemporalStrataSerializer,
)
from ..permissions import IsPrjLeadOrAdminOrReadOnly

from ..filters import FN022Filter
from ..permissions import ReadOnly
from ..pagination import StandardResultsSetPagination


class SeasonList(generics.ListAPIView):
    """an api end point to list all of the seasons (FN022) associated with a
    creel."""

    serializer_class = FN022Serializer

    def get_queryset(self):
        """ """

        prj_cd = self.kwargs.get("prj_cd")
        return FN022.objects.filter(creel__slug=prj_cd.lower()).select_related("creel")


class SeasonDetail(generics.RetrieveUpdateDestroyAPIView):
    """An api endpoint for get, put and delete endpoints for season
    objects associated with a specfic creel"""

    lookup_field = "ssn"
    serializer_class = FN022Serializer
    permission_classes = [IsPrjLeadOrAdminOrReadOnly]

    def get_queryset(self):
        """return only those season objects associate with this creel."""

        prj_cd = self.kwargs.get("prj_cd")
        return FN022.objects.filter(creel__slug=prj_cd.lower()).select_related("creel")


class TemporalStrataList(generics.ListAPIView):
    """an api end point to list all of the temporal strata in a creel as a single,
    nested object.
    """

    serializer_class = TemporalStrataSerializer

    def get_queryset(self):
        """ """

        prj_cd = self.kwargs.get("prj_cd")
        return (
            FN022.objects.filter(creel__slug=prj_cd.lower())
            .select_related("creel")
            .prefetch_related("exception_dates", "daytypes", "daytypes__periods")
        )


class FN022ListView(generics.ListAPIView):
    """A readonly enpoint to return FN022 - season strata data in format
    that closely matches FN-portal and FN-2 schema.."""

    serializer_class = FN022ListSerializer
    filterset_class = FN022Filter
    pagination_class = StandardResultsSetPagination
    permission_classes = [ReadOnly]

    def get_queryset(self):
        """"""
        return (
            FN022.objects.all()
            .select_related("creel")
            .annotate(prj_cd=F("creel__prj_cd"))
            .values("prj_cd", "ssn", "ssn_des", "ssn_date0", "ssn_date1", "slug", "id")
        )
