from datetime import date, time, datetime
from typing import Optional
from enum import IntEnum
from pydantic import validator, confloat, conint, confloat, constr

from .utils import yr_to_year, string_to_float, strip_date
from .FNBase import FNBase

from enum import IntEnum


class AngMethEnum(IntEnum):
    still = 1
    jig = 2
    drift = 3
    troll = 4
    down_rig = 5
    spin_cast = 6
    fly_cast = 7
    other = 8


class AngVisEnum(IntEnum):
    permanent_resident = 1
    non_permanent_resident = 2
    day_tripper = 3
    camp_provincial_park = 4
    camp_commercial_park = 5
    camp_crown_land = 6
    other_paid = 7
    other_non_paid = 8


class AngOrigEnum(IntEnum):
    local = 1
    ontario = 2
    canada = 3
    us = 4
    other = 5


class FN121(FNBase):
    """parser/validator for creel interview objects:

    + effdt0 must be constistent with prj_cd
    + effdt1 must be constistent with prj_cd and occur on or after effdt0

    """

    sama_id: int
    slug: str

    sam: constr(max_length=6)
    itvseq: conint(ge=1)
    itvtm0: time
    date: date
    efftm0: time
    efftm1: Optional[time]
    effcmp: bool = False

    effdur: Optional[confloat(gt=0)]
    persons: Optional[conint(ge=0)]
    anglers: Optional[conint(ge=0)]
    rods: Optional[conint(ge=0)]

    angmeth: Optional[AngMethEnum]
    angvis: Optional[AngVisEnum]
    angorig: Optional[AngOrigEnum]
    angop1: Optional[constr(max_length=25)]
    angop2: Optional[constr(max_length=25)]
    angop3: Optional[constr(max_length=25)]

    comment1: Optional[str]

    _string_to_float = validator(
        "effdur",
        allow_reuse=True,
        pre=True,
    )(string_to_float)

    _strip_date = validator(
        "itvtm0",
        "efftm0",
        "efftm1",
        allow_reuse=True,
        pre=True,
    )(strip_date)

    @validator("date")
    @classmethod
    def date_matches_prj_cd(cls, v, values):
        if v:
            prj_cd_yr = yr_to_year(values.get("slug", "")[6:8])
            date_yr = str(v.year)
            if prj_cd_yr != date_yr:
                err_msg = f"""Interview Date ({v}) is not consistent with prj_cd ({prj_cd_yr})."""
                raise ValueError(err_msg)
        return v

    # TODO -> figure out logic to allow fishing efforts that started yesterday
    # need effdt0 and efftm0 - not just time.

    # @validator("efftm1")
    # def efftm0_before_efftm1(cls, v, values):
    #    efftm0 = values.get("efftm0")
    #    if v and efftm0:
    #        if efftm0 > v:
    #            raise ValueError(
    #                f"Lift date (efftm1={v}) occurs before set date(efftm0={efftm0})."
    #            )
    #    return v

    @validator("effcmp")
    def effcmp_when_efftm1(cls, v, values):
        efftm1 = values.get("efftm1")
        if efftm1 and v is False:
            raise ValueError("effcmp should be True if efftm1 is populated.")
        return v
