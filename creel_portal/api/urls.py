"""
=============================================================
~/creel_portal/creel_portal/api/urls.py
 Created: 28 Mar 2020 18:01:00

 DESCRIPTION:

  api endpoint urls

 A. Cottrill
=============================================================
"""

from django.urls import include, path

from .views import (
    CreelList,
    CreelDetail,
    SeasonList,
    SeasonDetail,
    DayTypeList,
    DayTypeDetail,
    PeriodList,
    PeriodDetail,
    ExceptionDateList,
    ExceptionDateDetail,
    TemporalStrataList,
    FishingModeList,
    FishingModeDetail,
    SpaceList,
    SpaceDetail,
    ActivityCountList,
    InterviewLogList,
    InterviewList,
    FN011ListView,
    FN022ListView,
    FN023ListView,
    FN024ListView,
    FN025ListView,
    FN026ListView,
    FN028ListView,
    FN111ListView,
    FN112ListView,
    FN121ListView,
    FN123ListView,
    FN125ListView,
    FN125LampreyListView,
    FN125TagListView,
    FN126ListView,
    FN127ListView,
)

urlpatterns = [
    path("creels/", CreelList.as_view(), name="creel-list"),
    path("creel/<slug:slug>/", CreelDetail.as_view(), name="creel-detail"),
    path("creel/<str:prj_cd>/seasons", SeasonList.as_view(), name="season-list"),
    path(
        "creel/<str:prj_cd>/season/<str:ssn>",
        SeasonDetail.as_view(),
        name="season-detail",
    ),
    path(
        "creel/<str:prj_cd>/<str:ssn>/day_types/",
        DayTypeList.as_view(),
        name="day-type-list",
    ),
    path(
        "creel/<str:prj_cd>/<str:ssn>/day_type/<str:dtp>",
        DayTypeDetail.as_view(),
        name="day-type-detail",
    ),
    path(
        "creel/<str:prj_cd>/<str:ssn>/<str:dtp>/periods",
        PeriodList.as_view(),
        name="period-list",
    ),
    path(
        "creel/<str:prj_cd>/<str:ssn>/<str:dtp>/period/<str:prd>",
        PeriodDetail.as_view(),
        name="period-detail",
    ),
    path(
        "creel/<str:prj_cd>/<str:ssn>/exception_dates",
        ExceptionDateList.as_view(),
        name="exception-date-list",
    ),
    path(
        "creel/<str:prj_cd>/<str:ssn>/exception_date/<str:date>",
        ExceptionDateDetail.as_view(),
        name="exception-date-detail",
    ),
    path(
        "creel/<str:prj_cd>/temporal_strata",
        TemporalStrataList.as_view(),
        name="temporal-strata-list",
    ),
    path("creel/<str:prj_cd>/spatial_strata", SpaceList.as_view(), name="space-list"),
    path(
        "creel/<str:prj_cd>/space/<str:space>",
        SpaceDetail.as_view(),
        name="space-detail",
    ),
    path(
        "creel/<str:prj_cd>/fishing_modes",
        FishingModeList.as_view(),
        name="fishing-mode-list",
    ),
    path(
        "creel/<str:prj_cd>/fishing_mode/<str:mode>",
        FishingModeDetail.as_view(),
        name="fishing-mode-detail",
    ),
    path(
        "creel/<str:prj_cd>/interview_logs",
        InterviewLogList.as_view(),
        name="interview-log-list",
    ),
    path(
        "creel/<str:prj_cd>/<str:sama>/activity_counts",
        ActivityCountList.as_view(),
        name="activity-count-list",
    ),
    path(
        "creel/<str:prj_cd>/interviews", InterviewList.as_view(), name="interview-list"
    ),
    path("sc011/", FN011ListView.as_view(), name="fn011-list"),
    path("sc022/", FN022ListView.as_view(), name="fn022-list"),
    path("sc023/", FN023ListView.as_view(), name="fn023-list"),
    path("sc024/", FN024ListView.as_view(), name="fn024-list"),
    path("sc025/", FN025ListView.as_view(), name="fn025-list"),
    path("sc026/", FN026ListView.as_view(), name="fn026-list"),
    path("sc028/", FN028ListView.as_view(), name="fn028-list"),
    path("sc111/", FN111ListView.as_view(), name="fn111-list"),
    path("sc112/", FN112ListView.as_view(), name="fn112-list"),
    path("sc121/", FN121ListView.as_view(), name="fn121-list"),
    path("sc123/", FN123ListView.as_view(), name="fn123-list"),
    path("sc125/", FN125ListView.as_view(), name="fn125-list"),
    path("sc125lamprey/", FN125LampreyListView.as_view(), name="fn125-lamprey-list"),
    path("sc125tags/", FN125TagListView.as_view(), name="fn125-tag-list"),
    path("sc126/", FN126ListView.as_view(), name="fn126-list"),
    path("sc127/", FN127ListView.as_view(), name="fn127-list"),
]
