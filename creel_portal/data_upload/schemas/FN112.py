from datetime import datetime, time, date
from enum import IntEnum
from typing import Optional

from pydantic import validator, constr, confloat, conint


from .FNBase import FNBase
from .utils import not_specified, string_to_float, to_uppercase, strip_date


class FN112(FNBase):
    """Activity Count"""

    slug: str
    sama_id: int

    atytm0: time
    atytm1: time
    atydur: confloat(ge=0)

    atycnt: conint(ge=0) = 0
    itvcnt: conint(ge=0) = 0
    chkcnt: Optional[conint(ge=0)] = 0

    class Config:
        validate_assignment = True

    _strip_date = validator(
        "atytm0",
        "atytm1",
        allow_reuse=True,
        pre=True,
    )(strip_date)

    @validator("atytm1")
    def atytm0_before_atytm1(cls, v, values):
        atytm0 = values.get("atytm0")
        if v and atytm0:
            if atytm0 > v:
                start = atytm0.strftime("%H:%M")
                end = v.strftime("%H:%M")
                raise ValueError(
                    f"Activity Count end time (atytm1={end}) occurs before start time(atytm0={start})."
                )
        return v

    # atydur is calcuated on data upload, not externally so there is no
    # need to check it right now.


#    @validator("atydur")
#    def atydur_matches_atytm0_atytm1(cls, v, values):
#        """verify that the period duration is consistent with difference between the times"""
#        atytm0 = values.get("atytm0")
#        atytm1 = values.get("atytm1")
#        today = date.today()
#
#        if atytm0 and atytm1:
#            delta = datetime.combine(today, atytm1) - datetime.combine(today, atytm0)
#            delta_hours = delta.seconds / 3600
#            if v is None:
#                return delta_hours
#            if round(delta_hours, 1) != round(v, 1):
#                start = atytm0.strftime("%H:%M")
#                end = atytm1.strftime("%H:%M")
#                err_msg = (
#                    f"Activity duration (atydur={v}) is not consistent with start "
#                    + f"and end times({start}, {end}, delta={delta_hours})."
#                )
#                raise ValueError(err_msg)
#        return v
