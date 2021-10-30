from rest_framework import serializers

from ...models.creel import FN025


class FN025Serializer(serializers.ModelSerializer):
    """Class to serialize the exception dates within seasons within each creel."""

    class Meta:
        model = FN025
        fields = ("slug", "season", "date", "dtp1", "description")
