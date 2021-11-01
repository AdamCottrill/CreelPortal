from django.db.models import F
from rest_framework import generics

from ...models import FN125_Tag
from ..filters import FN125TagFilter
from ..serializers import FN125TagListSerializer
from ..permissions import ReadOnly
from ..pagination import StandardResultsSetPagination


class FN125TagListView(generics.ListAPIView):
    """A readonly enpoint to return FN125Tag - season strata data in format
    that closely matches FN-portal and FN-2 schema.."""

    serializer_class = FN125TagListSerializer
    filterset_class = FN125TagFilter
    pagination_class = StandardResultsSetPagination
    permission_classes = [ReadOnly]

    def get_queryset(self):
        """"""
        return (
            FN125_Tag.objects.select_related(
                "fish",
                "fish__catch",
                "fish__catch__interview",
                "fish__catch__interview__sama",
                "fish__catch__interview__sama__creel",
            )
            .annotate(
                prj_cd=F("fish__catch__interview__sama__creel__prj_cd"),
                sam=F("fish__catch__interview__sam"),
                spc=F("fish__catch__species__spc"),
                grp=F("fish__catch__grp"),
                _fish=F("fish__fish"),
            )
            .order_by("slug")
            .values(
                "prj_cd",
                "sam",
                "spc",
                "grp",
                "_fish",
                "fish_tag_id",
                "tagstat",
                "tagid",
                "tagdoc",
                "xcwtseq",
                "xtaginckd",
                "xtag_chk",
                "slug",
                "id",
            )
        )
