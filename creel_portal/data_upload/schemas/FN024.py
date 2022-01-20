from datetime import datetime, date, time
from typing import Optional
from pydantic import validator, constr, confloat
from .utils import strip_date
from .FNBase import FNBase


class FN024(FNBase):
    """Periods - within daytype."""

    slug: str
    daytype_id: int

    prd: constr(regex="^([A-Z0-9]{2})$", max_length=2)
    prdtm0: time
    prdtm1: time
    prd_dur: confloat(ge=0)

    class Config:
        validate_assignment = True

    _strip_date = validator(
        "prdtm0",
        "prdtm1",
        pre=True,
    )(strip_date)

    @validator("prdtm1")
    def prdtm0_before_prdtm1(cls, v, values):
        prdtm0 = values.get("prdtm0")
        if v and prdtm0:
            if prdtm0 > v:
                start = prdtm0.strftime("%H:%M")
                end = v.strftime("%H:%M")
                raise ValueError(
                    f"Period end time (prdtm1={end}) occurs before start time(prdtm0={start}).",
                )
        return v

    @validator("prd_dur")
    def prd_dur_matches_prdtm0_prdtm1(cls, v, values):
        """verify that the period duration is consistent with difference between the times"""
        prdtm0 = values.get("prdtm0")
        prdtm1 = values.get("prdtm1")
        today = date.today()

        if prdtm0 and prdtm1:
            delta = datetime.combine(today, prdtm1) - datetime.combine(today, prdtm0)
            delta_hours = delta.seconds / 3600
            if delta_hours != v:
                start = prdtm0.strftime("%H:%M")
                end = prdtm1.strftime("%H:%M")
                err_msg = (
                    f"Period duration (prd_dur={v}) is not consistent with period start "
                    + f"and end ({start}, {end}, delta={delta_hours})."
                )
                raise ValueError(err_msg)
        return v
