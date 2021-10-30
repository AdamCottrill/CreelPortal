from rest_framework import serializers

from ...models.creel import FN028


class FN028Serializer(serializers.ModelSerializer):
    class Meta:
        model = FN028
        fields = ("slug", "creel", "mode", "mode_des", "atyunit", "itvunit", "chkflag")
