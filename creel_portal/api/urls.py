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
    SeasonList,
    DayTypeList,
    PeriodList,
    ExceptionDateList,
    TemporalStrataList,
    FishingModeList,
    SpaceList,
    ActivityCountList,
    InterviewLogList,
    InterviewList,
)

urlpatterns = [
    path("creels/", CreelList.as_view(), name="creel-list"),
    path("creel/<str:prj_cd>/seasons", SeasonList.as_view(), name="season-list"),
    path(
        "creel/<str:prj_cd>/day_types/<str:ssn>",
        DayTypeList.as_view(),
        name="day-type-list",
    ),
    path(
        "creel/<str:prj_cd>/periods/<str:ssn>/<str:dtp>",
        PeriodList.as_view(),
        name="period-list",
    ),
    path(
        "creel/<str:prj_cd>/exception_dates/<str:ssn>/",
        ExceptionDateList.as_view(),
        name="exception-date-list",
    ),
    path(
        "creel/<str:prj_cd>/temporal_strata",
        TemporalStrataList.as_view(),
        name="temporal-strata-list",
    ),
    path("creel/<str:prj_cd>/spatial_strata", SpaceList.as_view(), name="space-list"),
    path(
        "creel/<str:prj_cd>/fishing_modes",
        FishingModeList.as_view(),
        name="fishing-mode-list",
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
]
