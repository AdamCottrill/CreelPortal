from rest_framework import serializers

from creel_portal.models import Lake, Species, FR713, FR714


class LakeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lake
        fields = ('id', 'lake_name', 'abbrev')


class SpeciesSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Species
        fields = ('id', 'species_code', 'common_name', 'scientific_name')


class FR713Serializer(serializers.ModelSerializer):

    mode = serializers.CharField(source='mode.mode', read_only=True)
    season = serializers.CharField(source='ssn.ssn', read_only=True)
    dtp = serializers.CharField(source='dtp.dtp', read_only=True)
    period = serializers.CharField(source='period.prd', read_only=True)
    area = serializers.CharField(source='area.space', read_only=True)

    class Meta:
        model = FR713
        fields = ('id', 'mode', 'season', 'dtp', 'period', 'area',
                  'effre', 'effae', 'effao_s', 'effro_s')


class FR714Serializer(serializers.ModelSerializer):

    mode = serializers.CharField(source='mode.mode', read_only=True)
    season = serializers.CharField(source='ssn.ssn', read_only=True)
    dtp = serializers.CharField(source='dtp.dtp_nm', read_only=True)
    period = serializers.CharField(source='period.prd', read_only=True)
    area = serializers.CharField(source='area.space', read_only=True)
    species = serializers.CharField(source='species.common_name',
                                    read_only=True)

    class Meta:
        model = FR714
        fields = ('id', 'mode', 'season', 'dtp', 'period', 'area', 'species',
                  'sek', 'catne', 'catne1', 'hvsno_s', 'hvsno1_s', 'hvsne',
                  'hvsne1')
