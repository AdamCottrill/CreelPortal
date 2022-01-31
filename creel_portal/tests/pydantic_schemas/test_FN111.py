"""=============================================================
 c:/Users/COTTRILLAD/1work/Python/pydantic_playground/tests/test_FN111.py
 Created: 26 Aug 2021 16:43:50

 DESCRIPTION:

  A suite of unit tests to ensure that the Pydantic model for FN111
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

from datetime import datetime, time
import pytest
from pydantic import ValidationError

from creel_portal.data_upload.schemas import FN111


@pytest.fixture()
def data():
    data = {
        "slug": "lha_ia19_002-1-001",
        "creel_id": 1,
        "season_id": 10,
        "daytype_id": 10,
        "period_id": 10,
        "area_id": 10,
        "mode_id": 10,
        "sama": "12345",
        "date": datetime(2022, 1, 19),
        "samtm0": time(11, 00),
        "weather": 0,
        "comment1": "This is a fake comment",
        "dow": 4,
    }
    return data


def test_valid_data(data):
    """

    Arguments:
    - `data`:
    """

    item = FN111(**data)

    assert item.creel_id == data["creel_id"]
    assert item.slug == data["slug"]


required_fields = [
    "slug",
    "creel_id",
    "season_id",
    "daytype_id",
    "period_id",
    "area_id",
    "mode_id",
    "sama",
    "date",
    "samtm0",
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
        FN111(**data)
    msg = "none is not an allowed value"
    assert msg in str(excinfo.value)


optional_fields = [
    "comment2",
    "weather",
]


@pytest.mark.parametrize("fld", optional_fields)
def test_optional_fields(data, fld):
    """Verify that the FN111 item is created without error if an optional field is omitted

    Arguments:
    - `data`:

    """
    data[fld] = None
    item = FN111(**data)
    assert item.creel_id == data["creel_id"]


# invalid sama - to long 123456789
# invalid date - foobar, April 31, 2019
# invalid time - foobar, -9:00
# invalid weather - cloudy
# invalide dow

error_list = [
    (
        "sama",
        "1234567",
        "ensure this value has at most 6 characters",
    ),
    (
        "date",
        "2020-04-31",
        "invalid date format",
    ),
    (
        "date",
        "foobar",
        "invalid date format",
    ),
    (
        "samtm0",
        "foobar",
        "invalid time format",
    ),
    (
        "samtm0",
        "-9:00",
        "invalid time format",
    ),
    (
        "samtm0",
        "24:00",
        "invalid time format",
    ),
    (
        "samtm0",
        "24:11",
        "invalid time format",
    ),
    (
        "weather",
        "cloudy",
        "value is not a valid integer",
    ),
]


@pytest.mark.parametrize("fld,value,msg", error_list)
def test_invalid_data(data, fld, value, msg):
    """

    Arguments:
    - `data`:
    """

    data[fld] = value
    with pytest.raises(ValidationError) as excinfo:
        FN111(**data)

    assert msg in str(excinfo.value)
