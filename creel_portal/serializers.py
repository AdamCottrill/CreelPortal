from rest_framework import serializers

from creel_portal.models import Lake, Species
from creel_portal.models import *


class LakeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lake
        fields = ('id', 'lake_name', 'abbrev')


class SpeciesSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Species
        fields = ('id', 'species_code', 'common_name', 'scientific_name')


class FN011Serializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FN011
        fields = ('id', 'lake', 'prj_date0', 'prj_date1', 'prj_cd', 'year',
                  'prj_nm', 'prj_ldr', 'comment0', 'slug')


class FN022Serializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FN022
        fields = ('id', 'creel', 'ssn', 'ssn_des', 'ssn_date0', 'ssn_date1')


class FN023Serializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FN023
        fields = ('id', 'dtp', 'dtp_nm', 'dow_lst')


class FN024Serializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FN024
        fields = ('id', 'prd', 'prdtm0', 'prdtm1')


class FN025Serializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FN025
        fields = ('id', 'season', 'date', 'dtp1')


class FN026Serializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FN026
        fields = ('id', 'creel', 'space', 'space_des', 'space_siz',
                  'label', 'area_cnt', 'area_lst', 'area_wt',
                  'ddlat', 'ddlon')


class FN028Serializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FN028
        fields = ('id', 'creel', 'mode', 'mode_des', 'atyunit', 'itvunit',
                  'chkflag')



class FR711Serializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FR711
        fields = ('id', 'creel',
                  'run',
                  'atycrit',
                  'cifopt',
                  'contmeth',
                  'do_cif',
                  'fr71_est',
                  'fr71_unit',
                  'mask_c',
                  'save_daily',
                  'strat_comb')


class StrataSerializer(serializers.HyperlinkedModelSerializer):
    creel = serializers.CharField(source='creel_run.creel', read_only=True)
    run = serializers.CharField(source='creel_run.run', read_only=True)

    class Meta:
        model = Strata
        fields = ('id', 'creel', 'run','season', 'daytype',
                  'period', 'area', 'mode')


class FN111Serializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FN111
        fields = ('id', 'creel', 'area', 'mode', 'sama', 'date', 'samtm0',
                  'weather', 'help_str', 'comment1')

class FN112Serializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FN112
        fields = ('id', 'atytm0', 'atytm1', 'atycnt', 'chkcnt', 'itvcnt')


class FN121Serializer(serializers.HyperlinkedModelSerializer):

    creel = serializers.CharField(source='sama.creel', read_only=True)
    area = serializers.CharField(source='sama.area', read_only=True)
    mode = serializers.CharField(source='sama.mode', read_only=True)

    class Meta:
        model = FN121
        fields = ('id', 'creel', 'sama', 'area', 'mode', 'sam', 'itvseq',
                  'itvtm0', 'date', 'efftm0', 'efftm1', 'effcmp', 'effdur',
                  'persons', 'anglers', 'rods', 'angmeth', 'angvis',
                  'angorig', 'angop1', 'angop2', 'angop3', 'comment1')


class FN123Serializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FN123
        fields = ('id', 'interview', 'species', 'sek', 'hvscnt', 'rlscnt',
                  'mescnt', 'meswt')


class FN125Serializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FN125
        fields = ('id', 'catch', 'grp', 'fish', 'flen', 'tlen', 'rwt', 'sex',
                  'gon', 'mat', 'age', 'agest', 'clipc', 'fate')


class FN127Serializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FN127
        fields = ('id', 'fish', 'ageid', 'agea', 'agemt', 'conf', 'edge',
                  'nca')


class FR713Serializer(serializers.ModelSerializer):

    mode = serializers.CharField(source='stratum.mode.label', read_only=True)
    season = serializers.CharField(source='stratum.season.label',
                                   read_only=True)
    dtp = serializers.CharField(source='stratum.daytype.label', read_only=True)
    period = serializers.CharField(source='stratum.period.prd', read_only=True)
    area = serializers.CharField(source='stratum.area.label', read_only=True)
    ddlat = serializers.FloatField(source='stratum.area.ddlat', read_only=True)
    ddlon = serializers.FloatField(source='stratum.area.ddlon', read_only=True)

    class Meta:
        model = FR713
        fields = ('id', 'mode', 'season', 'dtp', 'period', 'area', 'date',
                  'effre', 'effae', 'effao_s', 'effro_s', 'ddlat', 'ddlon')


class FR714Serializer(serializers.ModelSerializer):


    mode = serializers.CharField(source='stratum.mode.label', read_only=True)
    season = serializers.CharField(source='stratum.season.label',
                                   read_only=True)
    dtp = serializers.CharField(source='stratum.daytype.label', read_only=True)
    period = serializers.CharField(source='stratum.period.prd', read_only=True)
    area = serializers.CharField(source='stratum.area.label', read_only=True)

    ddlat = serializers.FloatField(source='stratum.area.ddlat', read_only=True)
    ddlon = serializers.FloatField(source='stratum.area.ddlon', read_only=True)


    species = serializers.CharField(source='species.common_name',
                                    read_only=True)

    class Meta:
        model = FR714
        fields = ('id', 'mode', 'season', 'dtp', 'period', 'area', 'species',
                  'date', 'sek', 'catne', 'catne1', 'hvsno_s', 'hvsno1_s',
                  'hvsne', 'hvsne1', 'ddlat', 'ddlon')
