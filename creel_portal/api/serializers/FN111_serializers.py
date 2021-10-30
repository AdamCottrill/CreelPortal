from rest_framework import serializers

from ...models.creel import FN111

from .FN022_serializers import FN022Serializer
from .FN023_serializers import FN023Serializer
from .FN024_serializers import FN024Serializer
from .FN026_serializers import FN026Serializer
from .FN028_serializers import FN028Serializer
from .FN112_serializers import FN112Serializer


class FN111Serializer(serializers.ModelSerializer):
    """Class to serialize our creel logs, including any associated
    activity counts."""

    activity_counts = FN112Serializer(many=True, read_only=True)

    season = FN022Serializer(many=False)
    daytype = FN023Serializer(many=False)
    period = FN024Serializer(many=False)
    area = FN026Serializer(many=False)
    mode = FN028Serializer(many=False)

    class Meta:
        model = FN111
        fields = (
            "slug",
            "creel",
            "sama",
            "season",
            "daytype",
            "period",
            "area",
            "mode",
            "date",
            "samtm0",
            "weather",
            "comment1",
            "activity_counts",
        )
