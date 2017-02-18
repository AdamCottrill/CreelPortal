from django.shortcuts import render
from django.views.generic import ListView, DetailView

from creel_portal.models import FN011



class CreelListView(ListView):
    model = FN011
    template_name = "creel_portal/creel_list.html"


class CreelDetailView(DetailView):
    model = FN011
    template_name = "creel_portal/creel_detail.html"
    context_object_name = "creel"
