from rest_framework import serializers

from ...models.fishnet2 import FN123
from .common_serializers import SpeciesSerializer


class FN123Serializer(serializers.ModelSerializer):
    """Class to serialize catch counts  (FN123 records)"""

    species = SpeciesSerializer(many=False, read_only=True)

    class Meta:
        model = FN123
        fields = ("species", "sek", "hvscnt", "rlscnt", "mescnt", "meswt")
