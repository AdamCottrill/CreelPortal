from rest_framework import generics
from django.db.models import F

from ...models import FN024
from ..serializers import FN024Serializer, FN024ListSerializer
from ..permissions import IsPrjLeadOrAdminOrReadOnly, ReadOnly
from ..filters import FN024Filter

from ..pagination import StandardResultsSetPagination


class PeriodList(generics.ListAPIView):
    """an api end point to list all of the periods (FN024) with daytypes
    (FN023) within seasons (FN022) of a creel.
    """

    serializer_class = FN024Serializer

    def get_queryset(self):
        """ """

        prj_cd = self.kwargs.get("prj_cd")
        ssn = self.kwargs.get("ssn")
        dtp = self.kwargs.get("dtp")

        return (
            FN024.objects.filter(daytype__season__creel__slug=prj_cd.lower())
            .filter(daytype__season__ssn=ssn)
            .filter(daytype__dtp=dtp)
        )


class PeriodDetail(generics.RetrieveUpdateDestroyAPIView):
    """An api endpoint for get, put and delete endpoints for period objects
    objects associated with a daytpye, within a season within a specfic creel"""

    lookup_field = "prd"
    serializer_class = FN024Serializer
    permission_classes = [IsPrjLeadOrAdminOrReadOnly]

    def get_queryset(self):
        """return only those season objects associate with this daytype,
        season and creel.

        """
        prj_cd = self.kwargs.get("prj_cd")
        ssn = self.kwargs.get("ssn")
        dtp = self.kwargs.get("dtp")

        return (
            FN024.objects.filter(daytype__season__creel__slug=prj_cd.lower())
            .filter(daytype__season__ssn=ssn)
            .filter(daytype__dtp=dtp)
        )


class FN024ListView(generics.ListAPIView):
    """A readonly enpoint to return FN024 - day types data in format
    that closely matches FN-portal and FN-2 schema.."""

    serializer_class = FN024ListSerializer
    filterset_class = FN024Filter
    pagination_class = StandardResultsSetPagination
    permission_classes = [ReadOnly]

    def get_queryset(self):
        """"""
        return (
            FN024.objects.all()
            .select_related("daytype", "daytype__season", "daytype__season__creel")
            .annotate(
                prj_cd=F("daytype__season__creel__prj_cd"),
                ssn=F("daytype__season__ssn"),
                dtp=F("daytype__dtp"),
            )
            .values(
                "prj_cd",
                "ssn",
                "dtp",
                "prd",
                "prdtm0",
                "prdtm1",
                "prd_dur",
                "slug",
                "id",
            )
        )
