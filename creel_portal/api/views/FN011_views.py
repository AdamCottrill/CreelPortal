"""=============================================================
~/creel_portal/creel_portal/api/views.py
 Created: 26 Mar 2020 16:18:44


 DESCRIPTION:

  This file contains all of the api end points associated with the
  creel portal django application.  Most of the endpoints are
  presented in pairs - one to list and create objects, one to
  retrieve, update and destroy.


 A. Cottrill
=============================================================

"""

from rest_framework import generics

from ...models import FN011
from ..filters import FN011Filter
from ..serializers import FN011Serializer
from ..permissions import IsPrjLeadOrAdminOrReadOnly


class CreelList(generics.ListAPIView):
    """an api end point to list all of our creels."""

    # add filter for lake, year, creel type, paginage by 20

    serializer_class = FN011Serializer
    queryset = FN011.objects.select_related("lake").all()

    filterset_class = FN011Filter


class CreelDetail(generics.RetrieveUpdateDestroyAPIView):
    """An api endpoint for get, put and delete endpoints for creel objects.
    """

    queryset = FN011.objects.all()
    lookup_field = "slug"
    serializer_class = FN011Serializer
    permission_classes = [IsPrjLeadOrAdminOrReadOnly]
