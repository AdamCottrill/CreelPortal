from django.db.models import F
from rest_framework import generics

from ...models import FN028
from ..serializers import FN028Serializer, FN028ListSerializer
from ..permissions import IsPrjLeadOrAdminOrReadOnly, ReadOnly
from ..filters import FN028Filter
from ..pagination import StandardResultsSetPagination


class FishingModeList(generics.ListAPIView):
    """an api end point to list all of the fishing modes (FN022) associated with a
    creel."""

    serializer_class = FN028Serializer

    def get_queryset(self):
        """ """

        prj_cd = self.kwargs.get("prj_cd")
        return FN028.objects.filter(creel__slug=prj_cd.lower())


class FishingModeDetail(generics.RetrieveUpdateDestroyAPIView):
    """An api endpoint for get, put and delete endpoints for fishing mode
    objects associated with a specfic creel.

    """

    lookup_field = "mode"
    serializer_class = FN028Serializer
    permission_classes = [IsPrjLeadOrAdminOrReadOnly]

    def get_queryset(self):
        """ """
        prj_cd = self.kwargs.get("prj_cd")
        return FN028.objects.filter(creel__slug=prj_cd.lower())


class FN028ListView(generics.ListAPIView):
    """A readonly enpoint to return FN028 - season strata data in format
    that closely matches FN-portal and FN-2 schema.."""

    serializer_class = FN028ListSerializer
    filterset_class = FN028Filter
    pagination_class = StandardResultsSetPagination
    permission_classes = [ReadOnly]

    def get_queryset(self):
        """"""
        return (
            FN028.objects.all()
            .select_related("creel")
            .annotate(prj_cd=F("creel__prj_cd"))
            .values(
                "prj_cd",
                "mode",
                "mode_des",
                "atyunit",
                "itvunit",
                "chkflag",
                "slug",
                "id",
            )
        )
