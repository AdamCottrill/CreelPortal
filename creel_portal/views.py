from django.shortcuts import render
from django.views.generic import ListView, DetailView

from creel_portal.models import FN011, Lake, Species, FR713, FR714

from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, generics

from creel_portal.serializers import (LakeSerializer, SpeciesSerializer,
                                      FR713Serializer, FR714Serializer)



class CreelListView(ListView):
    model = FN011
    template_name = "creel_portal/creel_list.html"


class CreelDetailView(DetailView):
    model = FN011
    template_name = "creel_portal/creel_detail.html"
    context_object_name = "creel"





#api

@api_view(['GET'])
def lake_collection(request):
    if request.method == 'GET':
        lakes = Lake.objects.all()
        serializer = LakeSerializer(lakes, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def lake_element(request, pk):
    try:
        lake = Lake.objects.get(pk=pk)
    except Lake.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = LakeSerializer(post)
        return Response(serializer.data)





class SpeciesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Species to be viewed or edited.
    """
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer
    #permission_classes = (IsAuthenticatedOrReadOnly,)



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
