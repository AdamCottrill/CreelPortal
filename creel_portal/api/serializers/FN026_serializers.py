from rest_framework import serializers

from ...models import FN026


class FN026Serializer(serializers.ModelSerializer):
    class Meta:
        model = FN026
        fields = (
            "slug",
            "creel",
            "space",
            "space_des",
            "space_siz",
            "label",
            "area_cnt",
            "area_lst",
            "area_wt",
            "ddlat",
            "ddlon",
        )


class FN026ListSerializer(serializers.ModelSerializer):
    """A class to list serializers. This is a readonly seralizer that return the data
    as expected from FN-II. Project is replaced by prj_cd.
    """

    prj_cd = serializers.CharField(read_only=True)

    class Meta:
        model = FN026
        fields = (
            "prj_cd",
            "space",
            "space_des",
            "space_siz",
            "area_cnt",
            "area_lst",
            "area_wt",
            "ddlat",
            "ddlon",
            "slug",
            "id",
        )
