from django.urls import path, include
from rest_framework import routers

from . import views
from . import api_views

prj_cd_regex = r"(?P<slug>[A-Za-z]{3}_[A-Za-z]{2}\d{2}_([A-Za-z]|\d){3})"


router = routers.DefaultRouter()
router.register(r"species", api_views.SpeciesViewSet)
router.register(r"lakes", api_views.LakeViewSet)
router.register(r"creels", api_views.CreelViewSet)
# strata
router.register(r"seasons", api_views.SeasonViewSet)
router.register(r"periods", api_views.PeriodViewSet)
router.register(r"day_types", api_views.DaytypeViewSet)
router.register(r"exception_dates", api_views.SeasonViewSet)
router.register(r"spatial_strata", api_views.SpaceViewSet)
router.register(r"fishing_modes", api_views.ModeViewSet)

# data tables
router.register(r"creel_runs", api_views.CreelRunViewSet)
router.register(r"strata", api_views.StrataViewSet)
router.register(r"interview_logs", api_views.InterviewLogViewSet)
router.register(r"activity_counts", api_views.ActivityCountViewSet)
router.register(r"interviews", api_views.InterviewViewSet)
router.register(r"catch_counts", api_views.CatchCountViewSet)
router.register(r"biosamples", api_views.BioSampleViewSet)
router.register(r"age_estimates", api_views.AgeEstimateViewSet)


urlpatterns = [
    path("", views.CreelListView.as_view(), name="creel_list",),
    path("", views.CreelListView.as_view(), name="home",),
    path("<str:lake>/", views.CreelListView.as_view(), name="creels_by_lake",),
    path(
        ("creel_detail/<slug:slug>/"),
        views.CreelDetailView.as_view(),
        name="creel_detail",
    ),
    path(
        ("effort_estimates/<slug:slug>/"),
        views.effort_estimates,
        name="effort_estimates_plots",
    ),
    path(
        ("catch_estimates/<slug:slug>/"),
        views.catch_estimates,
        name="catch_estimates_plots",
    ),
    path(
        ("edit_creel_space/<slug:slug>/<str:space>/"),
        views.edit_creel_space,
        name="edit_creel_space",
    ),
    # api urls
    path("api/v1/", include(router.urls)),
    path(
        ("api/v1/effort_estimates/<slug:slug>/"),
        api_views.EffortEstimates.as_view(),
        name="effort_estimates",
    ),
    path(
        ("api/v1/catch_estimates/<slug:slug>/"),
        api_views.CatchEstimates.as_view(),
        name="catch_estimates",
    ),
    path(
        ("api/v1/creel_spaces/<slug:slug>/"),
        api_views.CreelSpaces.as_view(),
        name="creel_spaces",
    ),
    # The real api:
    path(
        "api/", include(("creel_portal.api.urls", "creel-api"), namespace="creel-api")
    ),
]
