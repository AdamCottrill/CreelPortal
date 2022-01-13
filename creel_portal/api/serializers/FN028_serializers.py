from rest_framework import serializers

from ...models import FN028


class FN028Serializer(serializers.ModelSerializer):
    class Meta:
        model = FN028
        fields = ("slug", "creel", "mode", "mode_des", "atyunit", "itvunit", "chkflag")


class FN028ListSerializer(serializers.ModelSerializer):
    prj_cd = serializers.CharField(read_only=True)

    class Meta:
        model = FN028
        fields = (
            "prj_cd",
            "mode",
            "mode_des",
            "atyunit",
            "itvunit",
            "chkflag",
            "slug",
            "id",
        )
