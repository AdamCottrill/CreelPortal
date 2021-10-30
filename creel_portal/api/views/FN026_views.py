from rest_framework import generics

from ...models import FN026
from ..serializers import FN026Serializer
from ..permissions import IsPrjLeadOrAdminOrReadOnly


class SpaceList(generics.ListAPIView):
    """an api end point to list all of the spaces (FN026) associated with a
    creel."""

    serializer_class = FN026Serializer

    def get_queryset(self):
        """
        """

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
        """
        """
        prj_cd = self.kwargs.get("prj_cd")
        return FN026.objects.filter(creel__slug=prj_cd.lower())
