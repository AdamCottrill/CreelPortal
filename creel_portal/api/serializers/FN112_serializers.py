from rest_framework import serializers

from ...models.creel import FN112


class FN112Serializer(serializers.ModelSerializer):
    """Class to serialize the acivity counts associated with a creel log."""

    class Meta:
        model = FN112
        fields = ("slug", "atytm0", "atytm1", "atycnt", "chkcnt", "itvcnt")
