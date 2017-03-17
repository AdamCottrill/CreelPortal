from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.template import RequestContext
from django.shortcuts import  get_object_or_404
from django.db.models import Q


import json
from django.core.serializers.json import DjangoJSONEncoder


from creel_portal.models import FN011



class CreelListView(ListView):
    model = FN011
    template_name = "creel_portal/creel_list.html"

    def get_queryset(self, **kwargs):
        queryset = FN011.objects.order_by('lake','-prj_date0')
        self.lake = self.kwargs.get('lake')
        self.q = self.request.GET.get("q")

        if self.lake:
            queryset = queryset.filter(lake__lake_name=self.lake)

        if self.q:
            queryset = queryset.filter(Q(prj_cd__icontains=self.q) |
                                       Q(prj_nm__icontains=self.q))

        return queryset

    def get_context_data(self, **kwargs):
        context = super(CreelListView, self).get_context_data(**kwargs)
        context['lake'] = self.lake
        context['q'] = self.q
        return context


class CreelDetailView(DetailView):
    model = FN011
    template_name = "creel_portal/creel_detail.html"
    context_object_name = "creel"

    def get_context_data(self, **kwargs):
        context = super(CreelDetailView, self).get_context_data(**kwargs)

        #get our creel and add the space label lat and lon to the context
        # as a json string.

        creel = kwargs.get('object')
        spots = creel.spatial_strata.values('label', 'ddlon','ddlat')
        context['spaces'] = json.dumps(list(spots), cls=DjangoJSONEncoder)

        return context





def effort_estimates(request, slug):
    """

    Arguments:
    - `request`:
    """

    creel = get_object_or_404(FN011, slug=slug)

    spots = creel.spatial_strata.values('label', 'ddlon','ddlat')
    spots_json = json.dumps(list(spots), cls=DjangoJSONEncoder)

    return render(request,
                  'creel_portal/creel_effort_plots.html',
                  {'creel': creel, 'spaces':spots_json})


def catch_estimates(request, slug):
    """

    Arguments:
    - `request`:
    """

    creel = get_object_or_404(FN011, slug=slug)

    spots = creel.spatial_strata.values('label', 'ddlon','ddlat')
    spots_json = json.dumps(list(spots), cls=DjangoJSONEncoder)


    return render(request,
                  'creel_portal/creel_catch_plots.html',
                  {'creel': creel, 'spaces':spots_json})
