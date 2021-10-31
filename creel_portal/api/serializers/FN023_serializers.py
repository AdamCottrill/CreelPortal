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


class FN023ListSerializer(serializers.ModelSerializer):
    """This is a readonly seralizer that return the data
    as expected from FN-II. Project is replaced by prj_cd.
    """

    prj_cd = serializers.CharField(read_only=True)
    ssn = serializers.CharField(read_only=True)

    class Meta:
        model = FN023
        fields = ("prj_cd", "ssn", "dtp", "dtp_nm", "dow_lst", "slug", "id")
