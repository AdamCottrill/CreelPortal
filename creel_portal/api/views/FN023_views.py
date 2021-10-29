from rest_framework import generics

from ...models import FN023
from ..serializers import FN023Serializer
from ..permissions import IsPrjLeadOrAdminOrReadOnly


class DayTypeList(generics.ListAPIView):
    """an api end point to list all of the daytypes (FN023) associated with a
    creel."""

    serializer_class = FN023Serializer

    def get_queryset(self):
        """
        """

        prj_cd = self.kwargs.get("prj_cd")
        ssn = self.kwargs.get("ssn")
        return FN023.objects.filter(season__creel__slug=prj_cd.lower()).filter(
            season__ssn=ssn
        )


class DayTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    """An api endpoint for get, put and delete endpoints for daytype objects
    objects associated with a season within a specfic creel """

    lookup_field = "dtp"
    serializer_class = FN023Serializer
    permission_classes = [IsPrjLeadOrAdminOrReadOnly]

    def get_queryset(self):
        """return only those season objects associate with this creel.
        """
        prj_cd = self.kwargs.get("prj_cd")
        ssn = self.kwargs.get("ssn")
        return FN023.objects.filter(season__creel__slug=prj_cd.lower()).filter(
            season__ssn=ssn
        )
