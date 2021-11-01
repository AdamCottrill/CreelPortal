from rest_framework import serializers

from ...models.creel import FN112


class FN112Serializer(serializers.ModelSerializer):
    """Class to serialize the acivity counts associated with a creel log."""

    class Meta:
        model = FN112
        fields = ("slug", "atytm0", "atytm1", "atycnt", "chkcnt", "itvcnt")


class FN112ListSerializer(serializers.ModelSerializer):
    """A fast and flat serializer to return our activity logs in FN-II like format."""

    prj_cd = serializers.CharField(read_only=True)
    sama = serializers.CharField(read_only=True, source="_sama")

    class Meta:
        model = FN112
        fields = (
            "prj_cd",
            "sama",
            "atytm0",
            "atytm1",
            "atycnt",
            "chkcnt",
            "itvcnt",
            "atydur",
            "slug",
            "id",
        )
