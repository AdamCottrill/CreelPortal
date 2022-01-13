from rest_framework import serializers

from ...models import FN011

from .common_serializers import UserSerializer, LakeSerializer


class FN011Serializer(serializers.ModelSerializer):
    """A serializer for our FN011 - creel objects. It will contain nested
    user and lake objects.

    TODOs:

    + Add UserSerializer, CreelType
    + create and update methods to handle nested objects
    """

    prj_ldr = UserSerializer(many=False)
    field_crew = UserSerializer(many=True)
    lake = LakeSerializer(many=False)

    class Meta:
        model = FN011

        fields = (
            "slug",
            "lake",
            "prj_date0",
            "prj_date1",
            "prj_cd",
            "year",
            "prj_nm",
            "prj_ldr",
            "field_crew",
            "comment0",
            "contmeth",
            "slug",
        )


class FN011ReadOnlySerializer(serializers.ModelSerializer):
    """A serializer for our FN011 creel objects. It is readonly, fast and flat."""

    prj_ldr = serializers.CharField(read_only=True, source="_prj_ldr")
    lake = serializers.CharField(read_only=True, source="_lake")

    class Meta:
        model = FN011

        fields = (
            "slug",
            "lake",
            "prj_date0",
            "prj_date1",
            "prj_cd",
            "year",
            "prj_nm",
            "prj_ldr",
            # "field_crew",
            "comment0",
            "contmeth",
            "slug",
        )
