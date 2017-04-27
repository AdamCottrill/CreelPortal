from django.conf.urls import url, include
from rest_framework import routers

from . import views
from . import api_views

prj_cd_regex = r'(?P<slug>[A-Za-z]{3}_[A-Za-z]{2}\d{2}_([A-Za-z]|\d){3})'


router = routers.DefaultRouter()
router.register(r'species', api_views.SpeciesViewSet)
router.register(r'lakes', api_views.LakeViewSet)
router.register(r'creels', api_views.CreelViewSet)
#strata
router.register(r'seasons', api_views.SeasonViewSet)
router.register(r'periods', api_views.PeriodViewSet)
router.register(r'day_types', api_views.DaytypeViewSet)
router.register(r'exception_dates', api_views.SeasonViewSet)
router.register(r'spatial_strata', api_views.SpaceViewSet)
router.register(r'fishing_modes', api_views.ModeViewSet)

#data tables
router.register(r'creel_runs', api_views.CreelRunViewSet)
router.register(r'strata', api_views.StrataViewSet)
router.register(r'interview_logs', api_views.InterviewLogViewSet)
router.register(r'activity_counts', api_views.ActivityCountViewSet)
router.register(r'interviews', api_views.InterviewViewSet)
router.register(r'catch_counts', api_views.CatchCountViewSet)
router.register(r'biosamples', api_views.BioSampleViewSet)
router.register(r'age_estimates', api_views.AgeEstimateViewSet)



urlpatterns = [
    url(r'^$', views.CreelListView.as_view(),
        name='creel_list',),

    url(r'^$', views.CreelListView.as_view(),
        name='home',),


    url(r'^(?P<lake>[a-zA-Z]{1,10})/$', views.CreelListView.as_view(),
        name='creels_by_lake',),



    url((r'^creel_detail/' + prj_cd_regex + r'/$'),
        views.CreelDetailView.as_view(),
        name="creel_detail"),

        url((r'^effort_estimates/' + prj_cd_regex + r'/$'),
        views.effort_estimates,
        name="effort_estimates_plots"),

        url((r'^catch_estimates/' + prj_cd_regex + r'/$'),
        views.catch_estimates,
        name="catch_estimates_plots"),


    url((r'^edit_creel_space/' + prj_cd_regex + r'/(?P<space>[\w+]{2})/$'),
        views.edit_creel_space,
        name="edit_creel_space"),


    #api urls
    url(r'^api/v1/', include(router.urls)),

     url((r'^api/v1/effort_estimates/' + prj_cd_regex + r'/$'),
        api_views.EffortEstimates.as_view(), name='effort_estimates'),

    url((r'^api/v1/catch_estimates/' + prj_cd_regex + r'/$'),
        api_views.CatchEstimates.as_view(), name='catch_estimates'),


    url((r'^api/v1/creel_spaces/' + prj_cd_regex + r'/$'),
        api_views.CreelSpaces.as_view(), name='creel_spaces'),


]
