from rest_framework import serializers

from ...models.creel import FN025


class FN025Serializer(serializers.ModelSerializer):
    """Class to serialize the exception dates within seasons within each creel."""

    class Meta:
        model = FN025
        fields = ("slug", "season", "date", "dtp1", "description")


class FN025ListSerializer(serializers.ModelSerializer):
    """This is a readonly seralizer that return the data
    as expected from FN-II. Project is replaced by prj_cd.
    """

    prj_cd = serializers.CharField(read_only=True)
    ssn = serializers.CharField(read_only=True)

    class Meta:
        model = FN025
        fields = ("prj_cd", "ssn", "dtp1", "date", "description", "slug", "id")
