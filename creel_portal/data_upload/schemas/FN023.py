from datetime import date
from typing import Optional
from pydantic import validator

from enum import IntEnum, Enum

from .FNBase import FNBase


class DayTypeEnum(IntEnum):
    weekday = 1
    weekend = 2


class DayTypeNameEnum(str, Enum):
    weekday = "WEEKDAY"
    weekend = "WEEKEND"


class DowListEnum(str, Enum):
    weekday = "23456"
    weekend = "17"


class FN023(FNBase):
    """Daytypes - within season."""

    slug: str
    season_id: int

    dtp: DayTypeEnum
    dtp_nm: DayTypeNameEnum
    dow_lst: DowListEnum

    class Config:
        validate_assignment = True

    @validator("dtp_nm")
    @classmethod
    def dtp_nm_matches_dtp(cls, v, values):
        """verify that the day type name is consistent with day type"""
        dtp = values.get("dtp")
        name = DayTypeEnum(dtp).name
        if name != DayTypeNameEnum(v.upper()).name:
            err_msg = f"Day type code '{dtp}' ({name.upper()}) is not consistent with day type name ({v})."
            raise ValueError(err_msg)

        return v.upper()

    @validator("dow_lst")
    @classmethod
    def dow_lst_matches_dtp(cls, v, values):
        """verify that the day type list is consistent with day type code"""
        dtp = values.get("dtp")
        name = DayTypeEnum(dtp).name
        if name != DowListEnum(v).name:
            err_msg = f"Day type code '{dtp}' ({name.upper()}) is not consistent with dow list ({v})."
            raise ValueError(err_msg)
        return v
