from typing import Optional, Union

from pydantic import confloat, PositiveFloat, validator, constr

from .FNBase import FNBase
from .utils import not_specified, string_to_float, to_uppercase


class FN026(FNBase):

    slug: str
    creel_id: int

    space: constr(regex="^([A-Z0-9]{2})$", max_length=2)
    space_des: constr(strip_whitespace=True)
    area_lst: Optional[str]

    space_siz: Optional[int]
    area_cnt: Optional[int]
    area_lst: Optional[str]
    area_wt: Optional[float]
    # label: Optional[str]

    # Lake extents => BOX(-92.0940 41.3808,-76.0591 49.0158)
    dd_lat: Optional[confloat(ge=41.6, le=49.1)] = None
    dd_lon: Optional[confloat(ge=-89.6, le=-76.3)] = None

    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True

    _to_uppercase = validator("space", allow_reuse=True, pre=True)(to_uppercase)

    _to_titlecase = validator("space_des", "area_lst", allow_reuse=True, pre=True)(
        not_specified
    )

    _string_to_float = validator("dd_lat", "dd_lon", allow_reuse=True, pre=True)(
        string_to_float
    )

    @validator("dd_lat", "dd_lon", pre=True, allow_reuse=True)
    def strip_0(cls, v):
        """Lat and lon can be null, but they cannot be 0."""
        if v == 0:
            return None
        return v

    @validator("dd_lon", allow_reuse=True)
    def dd_lon_and_dd_lat(cls, v, values):
        """dd_lon and dd_lat are required if the other value is provided"""

        dd_lat = values.get("dd_lat")
        if dd_lat and v is None:
            raise ValueError("dd_lon is required if dd_lat is provided.")
        if v and dd_lat is None:
            raise ValueError("dd_lon must be null if dd_lat is null.")
        return v
