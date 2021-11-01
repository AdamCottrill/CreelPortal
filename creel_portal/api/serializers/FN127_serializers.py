from rest_framework import serializers

from ...models.fishnet2 import FN127


class FN127ListSerializer(serializers.ModelSerializer):
    """Class to serialize our age estimates - fast and flat, readonly, to
    emulate FN-2 data structure.

    """

    prj_cd = serializers.CharField(read_only=True)
    sam = serializers.CharField(read_only=True)
    spc = serializers.CharField(read_only=True)
    grp = serializers.CharField(read_only=True)
    fish = serializers.CharField(read_only=True, source="_fish")

    class Meta:
        model = FN127
        fields = (
            "prj_cd",
            "sam",
            "spc",
            "grp",
            "fish",
            "ageid",
            "agemt",
            "agea",
            "preferred",
            "conf",
            "nca",
            "edge",
            "agest",
            "comment7",
            "id",
            "slug",
        )
