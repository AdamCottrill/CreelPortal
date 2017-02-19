from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.template import RequestContext
from django.shortcuts import  get_object_or_404
from creel_portal.models import FN011



class CreelListView(ListView):
    model = FN011
    template_name = "creel_portal/creel_list.html"


class CreelDetailView(DetailView):
    model = FN011
    template_name = "creel_portal/creel_detail.html"
    context_object_name = "creel"



def effort_estimates(request, slug):
    """

    Arguments:
    - `request`:
    """

    creel = get_object_or_404(FN011, slug=slug)

    return render(request,
                  'creel_portal/creel_effort_plots.html',
                  {'creel': creel})
