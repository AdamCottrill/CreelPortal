from rest_framework import generics
from ...models import FN025
from ..serializers import FN025Serializer
from ..permissions import IsPrjLeadOrAdminOrReadOnly


class ExceptionDateList(generics.ListAPIView):
    """an api end point to list all the exception dates (FN025) in a creel (FN011).
    """

    serializer_class = FN025Serializer

    def get_queryset(self):
        """
        """

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
        """
        """

        prj_cd = self.kwargs.get("prj_cd")
        ssn = self.kwargs.get("ssn")

        return FN025.objects.filter(season__creel__slug=prj_cd.lower()).filter(
            season__ssn=ssn
        )
