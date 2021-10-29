from rest_framework import generics

from ...models import FN121
from ..filters import FN121Filter
from ..serializers import FN121Serializer


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
