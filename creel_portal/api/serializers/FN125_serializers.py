from rest_framework import serializers

from ...models.fishnet2 import FN125


class FN125Serializer(serializers.ModelSerializer):
    """Class to serialize biological samples (FN125 records)"""

    # tags = FN125TagsSerializer(many=True, read_only=True)
    # lamprey = FN125LampreySerializer(many=True, read_only=True)
    # FN126 = FN126Serializer(many=True, read_only=True)

    class Meta:
        model = FN125
        fields = (
            "fish",
            "flen",
            "tlen",
            "rwt",
            "sex",
            "gon",
            "mat",
            "clipc",
            "agest",
            "fate",
        )


class FN125ListSerializer(serializers.ModelSerializer):
    """Class to serialize our biodata - fast and flat, readonly, to
    emulate FN-2 data structure.  Tags, lamprey, and age estimates are
    returned by other serializers.

    """

    # activity_counts = FN112Serializer(many=True, read_only=True)
    prj_cd = serializers.CharField(read_only=True)
    sam = serializers.CharField(read_only=True)
    spc = serializers.CharField(read_only=True)
    grp = serializers.CharField(read_only=True)
    fish = serializers.CharField(read_only=True, source="_fish")

    class Meta:
        model = FN125
        fields = (
            "prj_cd",
            "sam",
            "spc",
            "grp",
            "fish",
            "flen",
            "tlen",
            "rwt",
            "sex",
            "gon",
            "mat",
            "age",
            "agest",
            "clipc",
            "fate",
            "slug",
            "id",
            "slug",
            "id",
        )
