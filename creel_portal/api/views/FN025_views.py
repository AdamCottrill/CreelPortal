from django.db.models import F
from rest_framework import generics
from ...models import FN025
from ..serializers import FN025Serializer, FN025ListSerializer
from ..permissions import IsPrjLeadOrAdminOrReadOnly, ReadOnly
from ..filters import FN025Filter
from ..pagination import StandardResultsSetPagination


class ExceptionDateList(generics.ListAPIView):
    """an api end point to list all the exception dates (FN025) in a creel (FN011)."""

    serializer_class = FN025Serializer

    def get_queryset(self):
        """ """

        prj_cd = self.kwargs.get("prj_cd")
        ssn = self.kwargs.get("ssn")

        return FN025.objects.filter(season__creel__slug=prj_cd.lower()).filter(
            season__ssn=ssn
        )


class ExceptionDateDetail(generics.RetrieveUpdateDestroyAPIView):
    """An api endpoint for get, put and delete endpoints for exception
    date objects objects associated with a season within a specfic
    creel

    """

    lookup_field = "date"
    serializer_class = FN025Serializer
    permission_classes = [IsPrjLeadOrAdminOrReadOnly]

    def get_queryset(self):
        """ """

        prj_cd = self.kwargs.get("prj_cd")
        ssn = self.kwargs.get("ssn")

        return FN025.objects.filter(season__creel__slug=prj_cd.lower()).filter(
            season__ssn=ssn
        )


class FN025ListView(generics.ListAPIView):
    """A readonly enpoint to return FN025 - day types data in format
    that closely matches FN-portal and FN-2 schema.."""

    serializer_class = FN025ListSerializer
    filterset_class = FN025Filter
    pagination_class = StandardResultsSetPagination
    permission_classes = [ReadOnly]

    def get_queryset(self):
        """"""
        return (
            FN025.objects.all()
            .select_related("season", "season__creel")
            .annotate(prj_cd=F("season__creel__prj_cd"), ssn=F("season__ssn"))
            .values("prj_cd", "ssn", "date", "dtp1", "description", "slug", "id")
        )
