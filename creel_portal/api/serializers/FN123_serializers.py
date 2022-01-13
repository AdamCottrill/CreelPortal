from rest_framework import serializers

from ...models import FN123
from .common_serializers import SpeciesSerializer


class FN123Serializer(serializers.ModelSerializer):
    """Class to serialize catch counts  (FN123 records)"""

    species = SpeciesSerializer(many=False, read_only=True)

    class Meta:
        model = FN123
        fields = ("species", "sek", "hvscnt", "rlscnt", "mescnt", "meswt")


class FN123ListSerializer(serializers.ModelSerializer):
    """Class to serialize our creel logs, including any associated
    activity counts."""

    # activity_counts = FN112Serializer(many=True, read_only=True)
    prj_cd = serializers.CharField(read_only=True)
    sam = serializers.CharField(read_only=True)
    spc = serializers.CharField(read_only=True)

    class Meta:
        model = FN123
        fields = (
            "prj_cd",
            "sam",
            "spc",
            "grp",
            "sek",
            "hvscnt",
            "rlscnt",
            "mescnt",
            "meswt",
            "slug",
            "id",
        )
