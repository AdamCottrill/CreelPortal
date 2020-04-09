"""=============================================================
~/creel_portal/creel_portal/api/serializers.py
 Created: 29 Mar 2020 08:37:49


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

from ..models.fishnet2 import FN011, FN121, FN123, FN125

from ..models.creel import FN022, FN023, FN024, FN025, FN026, FN028, FN111, FN112


User = get_user_model()

# we will need a user serializer here...


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
        fields = ("id", "species_code", "common_name", "scientific_name")


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


class FN022Serializer(serializers.ModelSerializer):
    """Class to serialize the seasons (temporal strata) used in each creel."""

    creel = serializers.SlugRelatedField(many=False, read_only=True, slug_field="slug")

    class Meta:
        model = FN022
        fields = ("slug", "creel", "ssn", "ssn_des", "ssn_date0", "ssn_date1")


class FN023Serializer(serializers.ModelSerializer):
    """Class to serialize the daytypes within a season (temporal strata)
    used in each creel."""

    class Meta:
        model = FN023
        fields = ("slug", "dtp", "dtp_nm", "dow_lst")


class FN024Serializer(serializers.ModelSerializer):
    """Class to serialize the periods associated with each day types within a season
    used in each creel."""

    class Meta:
        model = FN024
        fields = ("slug", "prd", "prdtm0", "prdtm1", "prd_dur")


class FN025Serializer(serializers.ModelSerializer):
    """Class to serialize the exception dates within seasons within each creel."""

    class Meta:
        model = FN025
        fields = ("slug", "season", "date", "dtp1", "description")


class NestedFN023Serializer(serializers.ModelSerializer):
    """Class to serialize the daytypes within a season (temporal strata) with the periods as nested objects
    within each daytype."""

    periods = FN024Serializer(many=True, read_only=True)

    class Meta:
        model = FN023
        fields = ("slug", "dtp", "dtp_nm", "dow_lst", "periods")


class TemporalStrataSerializer(serializers.ModelSerializer):
    """Class to serialize all of the temporal strata used in each creel as
    a single nested object."""

    creel = serializers.SlugRelatedField(many=False, read_only=True, slug_field="slug")
    exception_dates = FN025Serializer(many=True, read_only=True)
    daytypes = NestedFN023Serializer(many=True, read_only=True)

    class Meta:
        model = FN022
        fields = (
            "slug",
            "creel",
            "ssn",
            "ssn_des",
            "ssn_date0",
            "ssn_date1",
            "exception_dates",
            "daytypes",
        )


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


class FN028Serializer(serializers.ModelSerializer):
    class Meta:
        model = FN028
        fields = ("slug", "creel", "mode", "mode_des", "atyunit", "itvunit", "chkflag")


class FN112Serializer(serializers.ModelSerializer):
    """Class to serialize the acivity counts associated with a creel log."""

    class Meta:
        model = FN112
        fields = ("slug", "atytm0", "atytm1", "atycnt", "chkcnt", "itvcnt")


class FN111Serializer(serializers.ModelSerializer):
    """Class to serialize our creel logs, including any associated activity counts."""

    activity_counts = FN112Serializer(many=True, read_only=True)

    season = FN022Serializer(many=False)
    daytype = FN023Serializer(many=False)
    period = FN024Serializer(many=False)
    area = FN026Serializer(many=False)
    mode = FN028Serializer(many=False)

    class Meta:
        model = FN111
        fields = (
            "slug",
            "creel",
            "sama",
            "season",
            "daytype",
            "period",
            "area",
            "mode",
            "date",
            "samtm0",
            "weather",
            "comment1",
            "activity_counts",
        )


# These could be/shouldbe extended from a fishnet pp
# FN121
# FN123
# FN125
# FN125_TAGS
# FN125_LAM
# FN126
# FN127


class FN125Serializer(serializers.ModelSerializer):
    """Class to serialize biological samples (FN125 records)"""

    # tags = FN125TagsSerializer(many=True, read_only=True)
    # lamprey = FN125LampreySerializer(many=True, read_only=True)
    # FN126 = FN126Serializer(many=True, read_only=True)

    class Meta:
        model = FN125
        fields = (
            "fish",
            "flen",
            "tlen",
            "rwt",
            "sex",
            "gon",
            "mat",
            "clipc",
            "agest",
            "fate",
        )


class FN123Serializer(serializers.ModelSerializer):
    """Class to serialize catch counts  (FN123 records)"""

    species = SpeciesSerializer(many=False, read_only=True)

    class Meta:
        model = FN123
        fields = ("species", "sek", "hvscnt", "rlscnt", "mescnt", "meswt")


class FN121Serializer(serializers.ModelSerializer):
    """Class to serialize interviews (FN121 records).  Note that this
    serializer accepts nested objects to represent catch counts
    """

    catch_counts = FN123Serializer(many=True, read_only=False)

    class Meta:
        model = FN121
        fields = (
            "sama",
            "sam",
            "itvseq",
            "itvtm0",
            "date",
            "efftm0",
            "efftm1",
            "effcmp",
            "effdur",
            "persons",
            "anglers",
            "rods",
            "angmeth",
            "angvis",
            "angorig",
            "angop1",
            "angop2",
            "angop3",
            "comment1",
            "catch_counts",
        )
