"""=============================================================
 c:/Users/COTTRILLAD/1work/Python/pydantic_playground/tests/test_FN121.py
 Created: 25 Aug 2021 15:23:07

 DESCRIPTION:

  A suite of unit tests to ensure that the Pydantic model for FN121
  objects validate as expected.

  The script includes:

  1.  a dictionary that representes complete, valid data.

  2. a list of fields and associated modifications that should be
     automatically tranformed by Pydantic (e.g. trimming whitespaces
     and converting to title case)

  3. a list of required fields that are systematically omitted,

  4. and finally a list of changes to the dictionary of good data that
     invalidates it in a known way and verifies that pydantic raises
     the expected exception.

 A. Cottrill
=============================================================

"""


import pytest
from pydantic import ValidationError
from datetime import datetime, time

from creel_portal.data_upload.schemas import FN121


@pytest.fixture()
def data():
    data = {
        "slug": "lha_ia19_002-1-001-091-00-50",
        "sama_id": 1,
        "sam": 1,
        "itvseq": 1,
        "itvtm0": time(12, 15, 0),
        "date": datetime(2019, 8, 2),
        "efftm0": time(8, 0, 0),
        "efftm1": time(12, 0, 0),
        "effcmp": True,
        "effdur": 4.0,
        "persons": 2,
        "anglers": 2,
        "rods": 2,
        "angmeth": 2,
        "angvis": 1,
        "angorig": 1,
        "angop1": "Answer to option 1",
        "angop2": "Answer to option 2",
        "angop3": "Answer to option 3",
        "comment1": "not a real sample",
    }
    return data


def test_valid_data(data):
    """

    Arguments:
    - `data`:
    """

    item = FN121(**data)

    assert item.sama_id == data["sama_id"]
    assert item.slug == data["slug"]


required_fields = [
    "slug",
    "sama_id",
    "sam",
    "itvseq",
    "itvtm0",
    "date",
    "efftm0",
    "effcmp",
]


@pytest.mark.parametrize("fld", required_fields)
def test_required_fields(data, fld):
    """Verify that the required fields without custome error message
    raise the default messge if they are not provided.


    Arguments:
    - `data`:

    """

    data[fld] = None

    with pytest.raises(ValidationError) as excinfo:
        FN121(**data)
    msg = "none is not an allowed value"
    assert msg in str(excinfo.value)


optional_fields = [
    "efftm1",
    "effdur",
    "persons",
    "anglers",
    "rods",
    "angmeth",
    "angvis",
    "angorig",
    "angop1",
    "angop2",
    "angop3",
    "comment1",
]


@pytest.mark.parametrize("fld", optional_fields)
def test_optional_fields(data, fld):
    """Verify that the FN121 item is created without error if an optional field is omitted

    Arguments:
    - `data`:

    """
    data[fld] = None
    item = FN121(**data)
    assert item.sama_id == data["sama_id"]


error_list = [
    (
        "sam",
        "1234567",
        "ensure this value has at most 6 characters",
    ),
    (
        "itvseq",
        -1,
        "ensure this value is greater than or equal to 1",
    ),
    (
        "itvtm0",
        "foobar",
        "validation error for FN121\nitvtm0\n  invalid time format",
    ),
    (
        "date",
        "foobar",
        "validation error for FN121\ndate\n  invalid date format",
    ),
    (
        "efftm0",
        "foobar",
        "validation error for FN121\nefftm0\n  invalid time format",
    ),
    (
        "efftm1",
        "foobar",
        "validation error for FN121\nefftm1\n  invalid time format",
    ),
    (
        "persons",
        -1,
        "ensure this value is greater than or equal to 0",
    ),
    (
        "anglers",
        -1,
        "ensure this value is greater than or equal to 0",
    ),
    (
        "rods",
        -1,
        "ensure this value is greater than or equal to 0",
    ),
    (
        "angmeth",
        99,
        "value is not a valid enumeration member;",
    ),
    (
        "angvis",
        99,
        "value is not a valid enumeration member;",
    ),
    (
        "angorig",
        99,
        "value is not a valid enumeration member;",
    ),
    ("effcmp", False, "effcmp should be True if efftm1 is populated."),
]


@pytest.mark.parametrize("fld,value,msg", error_list)
def test_invalid_data(data, fld, value, msg):
    """

    Arguments:
    - `data`:
    """

    data[fld] = value
    with pytest.raises(ValidationError) as excinfo:
        FN121(**data)

    assert msg in str(excinfo.value)
