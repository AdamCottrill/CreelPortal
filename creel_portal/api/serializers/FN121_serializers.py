from rest_framework import serializers

from ...models.fishnet2 import FN121
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
