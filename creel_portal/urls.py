from django.conf.urls import url, include
from rest_framework import routers

from . import views

prj_cd_regex = r'(?P<slug>[A-Za-z]{3}_[A-Za-z]{2}\d{2}_([A-Za-z]|\d){3})'


router = routers.DefaultRouter()
router.register(r'species', views.SpeciesViewSet)

urlpatterns = [
    url(r'^$', views.CreelListView.as_view(),
        name='creel_list',),

    url(r'^$', views.CreelListView.as_view(),
        name='home',),

    url((r'^creel_detail/' + prj_cd_regex + r'/$'),
        views.CreelDetailView.as_view(),
        name="creel_detail"),

#    url(r'creel_detail/(?P<slug>[A-Za-z]{3}_[A-Za-z]{2}\d{2}_([A-Za-z]|\d){3})/$',
#        views.CreelDetailView.as_view(),
#        name="creel_detail"),


    url(r'^api/', include(router.urls)),
    url(r'^api/v1/lakes/$', views.lake_collection, name='lake_collection'),
    url(r'^api/v1/lakes/(?P<pk>[0-9]+)$', views.lake_element,
        name='lake_element'),

     url((r'^api/v1/effort_estimates/' + prj_cd_regex + r'/$'),
        views.EffortEstimates.as_view(), name='effort_estimates'),

    url((r'^api/v1/catch_estimates/' + prj_cd_regex + r'/$'),
        views.CatchEstimates.as_view(), name='catch_estimates'),


]
