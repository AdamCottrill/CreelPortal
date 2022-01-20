"""
=============================================================
~/pydantic_playground/schemas/utils.py
Created: Jul-17-2021 17:44
DESCRIPTION:

    pydantic models used to parse and validate incoming records.

A. Cottrill
=============================================================
"""


from typing import Optional
from datetime import datetime


from pydantic.validators import str_validator


def string_to_float(v) -> Optional[float]:
    """A validator that will convert floats passed in as strings to a python float"""
    if v is None:
        return v
    else:
        try:
            val = float(v)
        except ValueError:
            val = None
    return val


def string_to_int(v) -> Optional[int]:
    """A validator that will convert floats passed in as strings to a python float"""
    if v is None:
        return v
    else:
        try:
            val = int(v)
        except ValueError:
            val = None
    return val


def empty_to_none(v: str) -> Optional[str]:
    if v == "":
        return None
    return v


class EmptyStrToNone(str):
    @classmethod
    def __get_validators__(cls):
        yield str_validator
        yield empty_to_none


def to_titlecase(value: str) -> str:
    if value:
        return value.title()
    else:
        return value


def to_uppercase(value: str) -> str:
    if value:
        return value.upper()
    else:
        return value


def not_specified(value: str) -> str:
    if value:
        return value.title()
    else:
        return "Not Specified"


def yr_to_year(yr):
    if int(yr) < 50:
        return f"20{yr}"
    else:
        return f"19{yr}"


def strip_date(value):
    """pyodbc treats times as datetimes. we need to strip the date off if
    it is there."""
    if isinstance(value, datetime):
        return value.time()
    return value
