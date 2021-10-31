from django.db.models import F
from rest_framework import generics

from ...models import FN023
from ..serializers import FN023Serializer, FN023ListSerializer
from ..permissions import IsPrjLeadOrAdminOrReadOnly, ReadOnly
from ..filters import FN023Filter

from ..pagination import StandardResultsSetPagination


class DayTypeList(generics.ListAPIView):
    """an api end point to list all of the daytypes (FN023) associated with a
    creel."""

    serializer_class = FN023Serializer

    def get_queryset(self):
        """ """

        prj_cd = self.kwargs.get("prj_cd")
        ssn = self.kwargs.get("ssn")
        return FN023.objects.filter(season__creel__slug=prj_cd.lower()).filter(
            season__ssn=ssn
        )


class DayTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    """An api endpoint for get, put and delete endpoints for daytype objects
    objects associated with a season within a specfic creel"""

    lookup_field = "dtp"
    serializer_class = FN023Serializer
    permission_classes = [IsPrjLeadOrAdminOrReadOnly]

    def get_queryset(self):
        """return only those season objects associate with this creel."""
        prj_cd = self.kwargs.get("prj_cd")
        ssn = self.kwargs.get("ssn")
        return FN023.objects.filter(season__creel__slug=prj_cd.lower()).filter(
            season__ssn=ssn
        )


class FN023ListView(generics.ListAPIView):
    """A readonly enpoint to return FN023 - day types data in format
    that closely matches FN-portal and FN-2 schema.."""

    serializer_class = FN023ListSerializer
    filterset_class = FN023Filter
    pagination_class = StandardResultsSetPagination
    permission_classes = [ReadOnly]

    def get_queryset(self):
        """"""
        return (
            FN023.objects.all()
            .select_related("season", "season__creel")
            .annotate(prj_cd=F("season__creel__prj_cd"), ssn=F("season__ssn"))
            .values("prj_cd", "ssn", "dtp", "dtp_nm", "dow_lst", "slug", "id")
        )
