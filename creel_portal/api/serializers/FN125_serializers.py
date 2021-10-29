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
