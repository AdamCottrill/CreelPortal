from rest_framework import generics

from ...models import FN111
from ..filters import FN111Filter
from ..serializers import FN111Serializer


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
