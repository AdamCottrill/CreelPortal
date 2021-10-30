from rest_framework import generics

from ...models import FN024
from ..serializers import FN024Serializer
from ..permissions import IsPrjLeadOrAdminOrReadOnly


class PeriodList(generics.ListAPIView):
    """an api end point to list all of the periods (FN024) with daytypes
    (FN023) within seasons (FN022) of a creel.
    """

    serializer_class = FN024Serializer

    def get_queryset(self):
        """
        """

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
    objects associated with a daytpye, within a season within a specfic creel """

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
