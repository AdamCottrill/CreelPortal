from datetime import datetime, time
from enum import IntEnum, Enum
from typing import Optional

from pydantic import PositiveFloat, validator, constr


from .FNBase import FNBase
from .utils import not_specified, string_to_float, to_uppercase


class ItvUnitEnum(IntEnum):
    """Interview Unit"""

    person = 1
    party = 2


class AtyUnitEnum(IntEnum):
    """Activity Unit"""

    person = 1
    party = 2


class ChkFlagEnum(IntEnum):
    """Check Count"""

    yes = 0
    no = 1


class FN028(FNBase):
    """fishing modes"""

    creel_id: int
    slug: str
    mode_des: Optional[str] = "Not Specified"
    mode: constr(regex="^([A-Z0-9]{2})$", max_length=2)

    atyunit: AtyUnitEnum
    itvunit: ItvUnitEnum
    chkflag: ChkFlagEnum

    class Config:
        validate_assignment = True

    _to_uppercase = validator("mode", allow_reuse=True, pre=True)(to_uppercase)

    _to_titlecase = validator("mode_des", allow_reuse=True, pre=True)(not_specified)

    @validator("itvunit")
    def itvunit_consistent_with_atyunit(cls, v, values):
        atyunit = values.get("atyunit")
        if atyunit == 2 and v != atyunit:
            msg = "If ATYUNIT=2, then ITVUNIT must also equal 2."
            raise ValueError(msg)
        return v
