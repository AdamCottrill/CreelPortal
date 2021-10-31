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
from django.db.models import F
from rest_framework import generics

from ...models import FN011
from ..filters import FN011Filter
from ..serializers import FN011Serializer, FN011ReadOnlySerializer
from ..permissions import IsPrjLeadOrAdminOrReadOnly, ReadOnly
from ..pagination import StandardResultsSetPagination


class CreelList(generics.ListAPIView):
    """an api end point to list all of our creels."""

    # add filter for lake, year, creel type, paginage by 20

    serializer_class = FN011Serializer
    queryset = FN011.objects.select_related("lake").all()

    filterset_class = FN011Filter


class CreelDetail(generics.RetrieveUpdateDestroyAPIView):
    """An api endpoint for get, put and delete endpoints for creel objects."""

    queryset = FN011.objects.all()
    lookup_field = "slug"
    serializer_class = FN011Serializer
    permission_classes = [IsPrjLeadOrAdminOrReadOnly]


class FN011ListView(generics.ListAPIView):
    """A readonly enpoint to return FN011 data in format that closely matches FN-portal and FN-2 schema.."""

    serializer_class = FN011ReadOnlySerializer
    filterset_class = FN011Filter
    pagination_class = StandardResultsSetPagination
    permission_classes = [ReadOnly]

    queryset = (
        FN011.objects.select_related("lake", "prj_ldr")
        .defer(
            "lake__geom",
            "lake__geom_ontario",
            "lake__envelope",
            "lake__envelope_ontario",
            "lake__centroid",
            "lake__centroid_ontario",
        )
        .all()
        .annotate(_prj_ldr=F("prj_ldr__username"), _lake=F("lake__abbrev"))
        .values(
            "slug",
            "_lake",
            "prj_date0",
            "prj_date1",
            "prj_cd",
            "year",
            "prj_nm",
            "_prj_ldr",
            "comment0",
            "contmeth",
            "slug",
        )
    )
