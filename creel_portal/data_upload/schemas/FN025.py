from datetime import date

from .FNBase import FNBase


class FN025(FNBase):
    """Exception Dates. (These must be within the season they are associated with.)"""

    slug: str
    season_id: int

    date: date

    class Config:
        validate_assignment = True
