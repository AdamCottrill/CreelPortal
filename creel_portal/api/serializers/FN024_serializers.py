from rest_framework import serializers

from ...models.creel import FN024


class FN024Serializer(serializers.ModelSerializer):
    """Class to serialize the periods associated with each day types within a season
    used in each creel."""

    class Meta:
        model = FN024
        fields = ("slug", "prd", "prdtm0", "prdtm1", "prd_dur")
