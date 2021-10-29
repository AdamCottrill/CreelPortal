from rest_framework import serializers

from ...models.creel import FN023

from .FN024_serializers import FN024Serializer


class FN023Serializer(serializers.ModelSerializer):
    """Class to serialize the daytypes within a season (temporal strata)
    used in each creel."""

    class Meta:
        model = FN023
        fields = ("slug", "dtp", "dtp_nm", "dow_lst")


class NestedFN023Serializer(serializers.ModelSerializer):
    """Class to serialize the daytypes within a season (temporal strata)
    with the periods as nested objects within each daytype.

    """

    periods = FN024Serializer(many=True, read_only=True)

    class Meta:
        model = FN023
        fields = ("slug", "dtp", "dtp_nm", "dow_lst", "periods")
