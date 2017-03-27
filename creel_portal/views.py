from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.template import RequestContext
from django.shortcuts import  get_object_or_404
from django.db.models import Q

import json
from django.core.serializers.json import DjangoJSONEncoder


from creel_portal.models import FN011, FN026
from creel_portal.forms import FN026Form



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



def edit_creel_space(request, slug, space):
    """
    Arguments:
    - `request`:
    - `slug`:
    - `space`:
    """

    space = get_object_or_404(FN026, creel__slug=slug, space=space)

    if request.method == 'POST':
        form = FN026Form(request.POST, instance=space)
        if form.is_valid():
            form.save()
            return redirect('creel_detail', slug=space.creel.slug)
    else:
        form = FN026Form(instance=space)

    return render(request,
                  'creel_portal/edit_creel_space.html',
                  {'form':form,
                   'space': space})




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
