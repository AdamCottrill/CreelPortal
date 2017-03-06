from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.template import RequestContext
from django.shortcuts import  get_object_or_404
from creel_portal.models import FN011



class CreelListView(ListView):
    model = FN011
    template_name = "creel_portal/creel_list.html"

    def get_queryset(self, **kwargs):
        queryset = FN011.objects.order_by('lake','-prj_date0')
        self.lake = self.kwargs.get('lake')

        if self.lake:
            queryset = queryset.filter(lake__lake_name=self.lake)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CreelListView, self).get_context_data(**kwargs)
        context['lake'] = self.lake
        return context


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


def catch_estimates(request, slug):
    """

    Arguments:
    - `request`:
    """

    creel = get_object_or_404(FN011, slug=slug)

    return render(request,
                  'creel_portal/creel_catch_plots.html',
                  {'creel': creel})
