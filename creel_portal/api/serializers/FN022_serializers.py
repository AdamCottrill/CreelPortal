from rest_framework import serializers

from ...models.creel import FN022
from .FN023_serializers import NestedFN023Serializer
from .FN025_serializers import FN025Serializer


class FN022Serializer(serializers.ModelSerializer):
    """Class to serialize the seasons (temporal strata) used in each creel."""

    creel = serializers.SlugRelatedField(many=False, read_only=True, slug_field="slug")

    class Meta:
        model = FN022
        fields = ("slug", "creel", "ssn", "ssn_des", "ssn_date0", "ssn_date1")


class TemporalStrataSerializer(serializers.ModelSerializer):
    """Class to serialize all of the temporal strata used in each creel as
    a single nested object.

    """

    creel = serializers.SlugRelatedField(many=False, read_only=True, slug_field="slug")
    exception_dates = FN025Serializer(many=True, read_only=True)
    daytypes = NestedFN023Serializer(many=True, read_only=True)

    class Meta:
        model = FN022
        fields = (
            "slug",
            "creel",
            "ssn",
            "ssn_des",
            "ssn_date0",
            "ssn_date1",
            "exception_dates",
            "daytypes",
        )
