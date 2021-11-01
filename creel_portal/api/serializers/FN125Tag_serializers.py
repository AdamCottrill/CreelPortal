from rest_framework import serializers

from ...models.fishnet2 import FN125_Tag


class FN125TagListSerializer(serializers.ModelSerializer):
    """Class to serialize our lamprey wounding data - fast and flat, readonly, to
    emulate FN-2 data structure.

    """

    prj_cd = serializers.CharField(read_only=True)
    sam = serializers.CharField(read_only=True)
    spc = serializers.CharField(read_only=True)
    grp = serializers.CharField(read_only=True)
    fish = serializers.CharField(read_only=True, source="_fish")

    class Meta:
        model = FN125_Tag
        fields = (
            "prj_cd",
            "sam",
            "spc",
            "grp",
            "fish",
            "fish_tag_id",
            "tagstat",
            "tagid",
            "tagdoc",
            "xcwtseq",
            "xtaginckd",
            "xtag_chk",
            "id",
            "slug",
        )
