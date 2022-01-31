from datetime import datetime, time, date
from enum import IntEnum
from typing import Optional

from pydantic import PositiveFloat, validator, constr


from .FNBase import FNBase
from .utils import not_specified, string_to_float, to_uppercase, strip_date


class WeatherEnum(IntEnum):
    """Weather"""

    no_effect = 0
    possible_effect = 1
    definite_effect = 2


# class DowEnum(IntEnum):
#     """Day of the week as a number"""

#     Sunday = 1
#     Monday = 2
#     Tuesday = 3
#     Wednesday = 4
#     Thursday = 5
#     Friday = 6
#     Saturday = 7


class FN111(FNBase):
    """Interview Logs"""

    slug: str
    creel_id: int
    season_id: int
    daytype_id: int
    period_id: int
    area_id: int
    mode_id: int

    sama: constr(max_length=6)
    date: date
    samtm0: time  # strip data
    weather: Optional[WeatherEnum]
    comment1: Optional[str]

    # # daycode:
    # dow: DowEnum

    class Config:
        validate_assignment = True

    _strip_date = validator(
        "samtm0",
        allow_reuse=True,
        pre=True,
    )(strip_date)

    # @validator("dow")
    # def dow_is_consistent_with_date(cls, v, values):
    #     date = values.get("date")
    #     if date:
    #         dow = int(date.strftime("%w")) + 1

    #         if dow != int(v):
    #             fdate = date.strftime("%Y-%m-%d")
    #             msg = (
    #                 f"DOW value ({v}) is not consistent with date ({fdate}, dow={dow})"
    #             )
    #             raise ValueError(msg)
    #     return v
