from rest_framework import serializers

from ...models import FN121
from .FN123_serializers import FN123Serializer


class FN121Serializer(serializers.ModelSerializer):
    """Class to serialize interviews (FN121 records).  Note that this
    serializer accepts nested objects to represent catch counts
    """

    catch_counts = FN123Serializer(many=True, read_only=False)

    class Meta:
        model = FN121
        fields = (
            "sama",
            "sam",
            "itvseq",
            "itvtm0",
            "date",
            "efftm0",
            "efftm1",
            "effcmp",
            "effdur",
            "persons",
            "anglers",
            "rods",
            "angmeth",
            "angvis",
            "angorig",
            "angop1",
            "angop2",
            "angop3",
            "comment1",
            "catch_counts",
        )


class FN121ListSerializer(serializers.ModelSerializer):
    """Class to serialize our creel logs, including any associated
    activity counts."""

    # activity_counts = FN112Serializer(many=True, read_only=True)
    prj_cd = serializers.CharField(read_only=True)
    sama = serializers.CharField(read_only=True, source="_sama")
    ssn = serializers.CharField(read_only=True)
    dtp = serializers.CharField(read_only=True)
    prd = serializers.CharField(read_only=True)
    space = serializers.CharField(read_only=True)
    mode = serializers.CharField(read_only=True)

    class Meta:
        model = FN121
        fields = (
            "prj_cd",
            "sama",
            "ssn",
            "dtp",
            "prd",
            "space",
            "mode",
            "sam",
            "itvseq",
            "itvtm0",
            "date",
            "efftm0",
            "efftm1",
            "effcmp",
            "effdur",
            "persons",
            "anglers",
            "rods",
            "angmeth",
            "angvis",
            "angorig",
            "angop1",
            "angop2",
            "angop3",
            "comment1",
            "slug",
            "id",
        )
