"""=============================================================
~/creel_portal/creel_portal/api/serializers/common_serializers.py
 Created: 28 Oct 2021 21:24:20

 DESCRIPTION:

  This files contains all of the serializers used by our front end api
  - essenially his is a re-do of the earlier api that does not appear
  to have been completed or tested.

# FN021 (?)


 A. Cottrill
=============================================================

"""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from common.models import Species, Lake

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]


class LakeSerializer(serializers.ModelSerializer):
    """A serializer for lake objects - this will eventually come from our
    common application."""

    class Meta:
        model = Lake
        fields = ("id", "lake_name", "abbrev")


class SpeciesSerializer(serializers.ModelSerializer):
    """A serialized for species objects - this will eventually come from our
    common application."""

    class Meta:
        model = Species
        fields = ("id", "spc", "spc_nmco", "spc_nmsc")
