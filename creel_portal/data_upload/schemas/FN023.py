from datetime import date
from typing import Optional
from pydantic import validator

from enum import IntEnum, Enum

from .FNBase import FNBase


class DayTypeEnum(IntEnum):
    weekday = 1
    weekend = 2


class DayTypeNameEnum(str, Enum):
    weekday = "Weekday"
    weekend = "Weekend"


class DayTypeListEnum(str, Enum):
    weekday = "23456"
    weekend = "17"


class FN023(FNBase):
    """Daytypes - within season."""

    slug: str
    season_id: int

    dtp: DayTypeEnum
    dtp_nm: DayTypeNameEnum
    dtp_lst: DayTypeListEnum

    class Config:
        validate_assignment = True

    @validator("dtp_nm")
    @classmethod
    def dtp_nm_matches_dtp(cls, v, values):
        """verify that the day type name is consistent with day type"""
        dtp = values.get("dtp")
        if DayTypeEnum(dtp).name != DayTypeNameEnum(v).name:

            err_msg = (
                f"Day type code ({dtp}) is not consistent with day type name ({v})."
            )
            raise ValueError(err_msg)

        return v

    @validator("dtp_lst")
    @classmethod
    def dtp_lst_matches_dtp(cls, v, values):
        """verify that the day type list is consistent with day type code"""
        dtp = values.get("dtp")
        if DayTypeEnum(dtp).name != DayTypeListEnum(v).name:
            err_msg = f"Day type code ({dtp}) is not consistent with day list ({v})."
            raise ValueError(err_msg)
        return v
