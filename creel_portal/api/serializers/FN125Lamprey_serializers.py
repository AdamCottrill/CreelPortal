from rest_framework import serializers

from ...models import FN125_Lamprey


class FN125LampreyListSerializer(serializers.ModelSerializer):
    """Class to serialize our lamprey wounding data - fast and flat, readonly, to
    emulate FN-2 data structure.

    """

    prj_cd = serializers.CharField(read_only=True)
    sam = serializers.CharField(read_only=True)
    spc = serializers.CharField(read_only=True)
    grp = serializers.CharField(read_only=True)
    fish = serializers.CharField(read_only=True, source="_fish")

    class Meta:
        model = FN125_Lamprey
        fields = (
            "prj_cd",
            "sam",
            "spc",
            "grp",
            "fish",
            "lamid",
            "xlam",
            "lamijc",
            "lamijc_type",
            "lamijc_size",
            "comment_lam",
            "id",
            "slug",
        )
