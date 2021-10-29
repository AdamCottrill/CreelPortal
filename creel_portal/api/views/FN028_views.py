from rest_framework import generics

from ...models import FN028
from ..serializers import FN028Serializer
from ..permissions import IsPrjLeadOrAdminOrReadOnly


class FishingModeList(generics.ListAPIView):
    """an api end point to list all of the fishing modes (FN022) associated with a
    creel."""

    serializer_class = FN028Serializer

    def get_queryset(self):
        """
        """

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
        """
        """
        prj_cd = self.kwargs.get("prj_cd")
        return FN028.objects.filter(creel__slug=prj_cd.lower())
