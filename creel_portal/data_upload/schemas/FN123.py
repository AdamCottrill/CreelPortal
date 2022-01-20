from typing import Optional
from enum import IntEnum
from pydantic import constr, conint, confloat, validator
from .FNBase import FNBase
from .utils import string_to_int, string_to_float


class SekEnum(IntEnum):
    no = 0
    yes = 1


class FN123(FNBase):
    """Pydantic model for FN123  - Catch Counts.

    slug, creel_id, species_id, and sek are all required fields.  All
    other fields are currently optional

    """

    slug: str
    interview_id: int
    species_id: int

    grp: constr(regex="^([A-Z0-9]{1,2})$", max_length=2)
    sek: SekEnum
    hvscnt: Optional[conint(ge=0)] = None
    rlscnt: Optional[conint(ge=0)] = None
    mescnt: Optional[conint(ge=0)] = None
    meswt: Optional[confloat(ge=0)] = None
    comment3: Optional[str]

    _string_to_float = validator("meswt", allow_reuse=True, pre=True)(string_to_float)

    _string_to_int = validator(
        "hvscnt", "rlscnt", "mescnt", allow_reuse=True, pre=True
    )(string_to_int)
