from rest_framework import serializers

from ...models import FN124


class FN124ListSerializer(serializers.ModelSerializer):

    prj_cd = serializers.CharField(read_only=True)
    sam = serializers.CharField(read_only=True)
    eff = serializers.CharField(read_only=True)
    spc = serializers.CharField(read_only=True)
    grp = serializers.CharField(read_only=True)

    class Meta:
        model = FN124
        fields = (
            "id",
            "prj_cd",
            "sam",
            "eff",
            "spc",
            "grp",
            "siz",
            "sizcnt",
            "slug",
        )

    def create(self, validated_data):
        """When we create new catch count object, we need to add the associated
        catch"""

        validated_data["catch"] = self.context["catch"]
        return FN124.objects.create(**validated_data)
