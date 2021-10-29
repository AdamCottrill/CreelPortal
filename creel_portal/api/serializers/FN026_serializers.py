from rest_framework import serializers

from ...models.creel import FN026


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
