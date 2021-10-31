from rest_framework import serializers

from ...models.creel import FN024


class FN024Serializer(serializers.ModelSerializer):
    """Class to serialize the periods associated with each day types within a season
    used in each creel."""

    class Meta:
        model = FN024
        fields = ("slug", "prd", "prdtm0", "prdtm1", "prd_dur")


class FN024ListSerializer(serializers.ModelSerializer):
    """This is a readonly seralizer that return the data
    as expected from FN-II. Project is replaced by prj_cd.
    """

    prj_cd = serializers.CharField(read_only=True)
    ssn = serializers.CharField(read_only=True)
    dtp = serializers.CharField(read_only=True)

    class Meta:
        model = FN024
        fields = (
            "prj_cd",
            "ssn",
            "dtp",
            "prd",
            "prdtm0",
            "prdtm1",
            "prd_dur",
            "slug",
            "id",
        )
