from django.db.models import F
from rest_framework import generics

from ...models import FN026
from ..serializers import FN026Serializer, FN026ListSerializer
from ..permissions import IsPrjLeadOrAdminOrReadOnly, ReadOnly
from ..filters import FN026Filter
from ..pagination import StandardResultsSetPagination


class SpaceList(generics.ListAPIView):
    """an api end point to list all of the spaces (FN026) associated with a
    creel."""

    serializer_class = FN026Serializer

    def get_queryset(self):
        """ """

        prj_cd = self.kwargs.get("prj_cd")
        return FN026.objects.filter(creel__slug=prj_cd.lower())


class SpaceDetail(generics.RetrieveUpdateDestroyAPIView):
    """An api endpoint for get, put and delete endpoints for
    space/area objects associated with a specfic creel

    """

    lookup_field = "space"
    serializer_class = FN026Serializer
    permission_classes = [IsPrjLeadOrAdminOrReadOnly]

    def get_queryset(self):
        """ """
        prj_cd = self.kwargs.get("prj_cd")
        return FN026.objects.filter(creel__slug=prj_cd.lower())


class FN026ListView(generics.ListAPIView):
    """A readonly enpoint to return FN026 - season strata data in format
    that closely matches FN-portal and FN-2 schema.."""

    serializer_class = FN026ListSerializer
    filterset_class = FN026Filter
    pagination_class = StandardResultsSetPagination
    permission_classes = [ReadOnly]

    def get_queryset(self):
        """"""
        return (
            FN026.objects.all()
            .select_related("creel")
            .annotate(prj_cd=F("creel__prj_cd"))
            .values(
                "prj_cd",
                "space",
                "space_des",
                "space_siz",
                "area_cnt",
                "area_lst",
                "area_wt",
                "ddlat",
                "ddlon",
                "slug",
                "id",
            )
        )
