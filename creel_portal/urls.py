from django.urls import path, include, re_path
from rest_framework import routers, permissions

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from . import views
from . import api_views

# readonly api endpoints:
from .api.urls import urlpatterns as api_urls

app_name = "creel_portal"

API_TITLE = "Creel Portal API"
API_DESC = "A Restful API for your Creel Survey Data"

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
    path(
        "data_upload/",
        view=views.creel_data_upload,
        name="upload_creel_data",
    ),
    # api urls
    path("api/v0/", include(router.urls)),
    path(
        ("api/v0/effort_estimates/<slug:slug>/"),
        # api_views.EffortEstimates.as_view(),
        views.effort_estimates_json,
        name="effort_estimates",
    ),
    path(
        ("api/v0/catch_estimates/<slug:slug>/"),
        # api_views.CatchEstimates.as_view(),
        views.catch_estimates_json,
        name="catch_estimates",
    ),
    path(
        ("api/v0/creel_spaces/<slug:slug>/"),
        api_views.CreelSpaces.as_view(),
        name="creel_spaces",
    ),
    # The real api:
    path(
        "api/v1/",
        include(("creel_portal.api.urls", "creel-api"), namespace="api"),
    ),
]


schema_view = get_schema_view(
    openapi.Info(
        title=API_TITLE,
        default_version="v1",
        description=API_DESC,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="adam.cottrill@ontario.ca"),
        license=openapi.License(name="BSD License"),
    ),
    # generate docs for all endpoint from here down:
    patterns=api_urls,
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns += [
    # =============================================
    #          API AND DOCUMENTATION
    # api documentation
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    #          API AND DOCUMENTATION
    path("", views.CreelListView.as_view(), name="home"),
    path("", views.CreelListView.as_view(), name="creel_list"),
    path("<str:lake>/", views.CreelListView.as_view(), name="creels_by_lake"),
]
