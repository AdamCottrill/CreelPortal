from rest_framework import viewsets, generics

from creel_portal.models import Lake, Species
from creel_portal.models import (FN011, FN022, FN023, FN024, FN025, FN026,
                                 FN028, FN111, FN112, FN121, FN123, FN125,
                                 FN127)
from creel_portal.models import FR713, FR714


# serializers for common elements
from creel_portal.serializers import LakeSerializer, SpeciesSerializer

#creel strata
from creel_portal.serializers import (FN011Serializer, FN022Serializer,
                                      FN023Serializer, FN024Serializer,
                                      FN025Serializer, FN026Serializer,
                                      FN028Serializer)
# data tables
from creel_portal.serializers import (FN111Serializer, FN112Serializer,
                                      FN121Serializer, FN123Serializer,
                                      FN125Serializer, FN127Serializer)

# creel results
from creel_portal.serializers import FR713Serializer, FR714Serializer


#==============================================
#    API-REST Views


class LakeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Lake to be viewed or edited.
    """
    queryset = Lake.objects.all()
    serializer_class = LakeSerializer



class SpeciesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Species to be viewed or edited.
    """
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer


class CreelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Creel (FN011) data  to be viewed or edited.
    """
    queryset = FN011.objects.all()
    serializer_class = FN011Serializer


class SeasonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Seasons to be viewed or edited.
    """
    queryset = FN022.objects.all()
    serializer_class = FN022Serializer


class DaytypeViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Daytypes used in a creel (season) to be
    viewed or edited.

    """
    queryset = FN023.objects.all()
    serializer_class = FN023Serializer


class PeriodViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Periods associated with a creel to be
    viewed or edited.

    """
    queryset = FN024.objects.all()
    serializer_class = FN024Serializer


class ExceptionDateViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Exception Dates associated with a creel to be
    viewed or edited.

    """
    queryset = FN025.objects.all()
    serializer_class = FN025Serializer


class SpaceViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Spatial strata  associated with a creel to be
    viewed or edited.

    """
    queryset = FN026.objects.all()
    serializer_class = FN026Serializer


class ModeViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Fishing Mode strata  associated with a creel
    to be viewed or edited.

    """
    queryset = FN028.objects.all()
    serializer_class = FN028Serializer



class InterviewLogViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Interview Logs associated with a creel
    to be viewed or edited.

    """
    queryset = FN111.objects.all()
    serializer_class = FN111Serializer


class ActivityCountViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Activity counts associated with a creel
    to be viewed or edited.

    """
    queryset = FN112.objects.all()
    serializer_class = FN112Serializer


class InterviewViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Interviews associated with a creel
    to be viewed or edited.

    """
    queryset = FN121.objects.all()
    serializer_class = FN121Serializer


class CatchCountViewSet(viewsets.ModelViewSet):
    """API endpoint that allows catch counts associated with a creel
    to be viewed or edited.

    """
    queryset = FN123.objects.all()
    serializer_class = FN123Serializer


class BioSampleViewSet(viewsets.ModelViewSet):
    """API endpoint that allows biological data associated with a creel
    to be viewed or edited.

    """
    queryset = FN125.objects.all()
    serializer_class = FN125Serializer


class AgeEstimateViewSet(viewsets.ModelViewSet):
    """API endpoint that allows age estimates associated with a creel
    to be viewed or edited.

    """
    queryset = FN127.objects.all()
    serializer_class = FN127Serializer




class EffortEstimates(generics.ListAPIView):
    serializer_class = FR713Serializer

    def get_queryset(self):
        """
        """
        slug = self.kwargs['slug']

        qs = FR713.objects.filter(creel__slug=slug).\
             exclude(strat__contains='+')

        return qs

class CatchEstimates(generics.ListAPIView):
    serializer_class = FR714Serializer

    def get_queryset(self):
        """
        """
        slug = self.kwargs['slug']

        qs = FR714.objects.filter(creel__slug=slug).\
             exclude(strat__contains='+')

        return qs
