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

from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response

from ..models import (
    FN011,
    FN022,
    FN023,
    FN024,
    FN025,
    FN026,
    FN028,
    FN111,
    FN112,
    FN121,
)

from .filters import FN011Filter, FN111Filter, FN121Filter

## original hyplinked serializers
# from ..serializers import (
#    # FN011Serializer,
#    # FN022Serializer,
#    # FN026Serializer,
#    # FN028Serializer,
#   # FN121Serializer,
# )

# new nested serializers
from .serializers import (
    FN011Serializer,
    FN022Serializer,
    FN023Serializer,
    FN024Serializer,
    FN025Serializer,
    FN026Serializer,
    FN028Serializer,
    TemporalStrataSerializer,
    FN111Serializer,
    FN112Serializer,
    FN121Serializer,
    FN123Serializer,
)


class CreelList(generics.ListAPIView):
    """an api end point to list all of our creels."""

    # add filter for lake, year, creel type, paginage by 20

    serializer_class = FN011Serializer
    queryset = FN011.objects.select_related("lake").all()

    filterset_class = FN011Filter


class SeasonList(generics.ListAPIView):
    """an api end point to list all of the seasons (FN022) associated with a
    creel."""

    serializer_class = FN022Serializer

    def get_queryset(self):
        """
        """

        prj_cd = self.kwargs.get("prj_cd")
        return FN022.objects.filter(creel__slug=prj_cd.lower()).select_related("creel")


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


class TemporalStrataList(generics.ListAPIView):
    """an api end point to list all of the temporal strata in a creel as a single,
    nested object.
    """

    serializer_class = TemporalStrataSerializer

    def get_queryset(self):
        """
        """

        prj_cd = self.kwargs.get("prj_cd")
        return (
            FN022.objects.filter(creel__slug=prj_cd.lower())
            .select_related("creel")
            .prefetch_related("exception_dates", "daytypes", "daytypes__periods")
        )


class SpaceList(generics.ListAPIView):
    """an api end point to list all of the spaces (FN026) associated with a
    creel."""

    serializer_class = FN026Serializer

    def get_queryset(self):
        """
        """

        prj_cd = self.kwargs.get("prj_cd")
        return FN026.objects.filter(creel__slug=prj_cd.lower())


class FishingModeList(generics.ListAPIView):
    """an api end point to list all of the fishing modes (FN022) associated with a
    creel."""

    serializer_class = FN028Serializer

    def get_queryset(self):
        """
        """

        prj_cd = self.kwargs.get("prj_cd")
        return FN028.objects.filter(creel__slug=prj_cd.lower())


class InterviewLogList(generics.ListAPIView):
    """an api end point to list all of the creel logs (FN111) associated with a
    creel."""

    serializer_class = FN111Serializer
    filter_class = FN111Filter

    def get_queryset(self):
        """
        """

        prj_cd = self.kwargs.get("prj_cd")
        return (
            FN111.objects.filter(creel__slug=prj_cd.lower())
            .prefetch_related("activity_counts")
            .select_related(
                "season", "season__creel", "period", "daytype", "area", "mode"
            )
        )


class ActivityCountList(generics.ListAPIView):
    """an api end point to list all of the activity Counts (Fn112)
    associated with an interview log (FN111) associated with a
    creel.

    These might be better as nested elements of the inteview logs.

    """

    serializer_class = FN111Serializer

    def get_queryset(self):
        """
        """

        prj_cd = self.kwargs.get("prj_cd")
        sama = self.kwargs.get("sama")

        return FN112.objects.filter(sama__creel__slug=prj_cd.lower(), sama__sama=sama)


class InterviewList(generics.ListAPIView):
    """an api end point to list all of the creel endpoints (FN121) associated with a
    creel."""

    serializer_class = FN121Serializer
    filter_class = FN121Filter

    def get_queryset(self):
        """
        """

        prj_cd = self.kwargs.get("prj_cd")
        return (
            FN121.objects.filter(sama__creel__slug=prj_cd.lower())
            .prefetch_related("catch_counts", "catch_counts__species")
            .select_related(
                "sama",
                "sama__season",
                "sama__season__creel",
                "sama__period",
                "sama__daytype",
                "sama__area",
                "sama__mode",
            )
        )
