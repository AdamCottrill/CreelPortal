"""=============================================================
 c:/Users/COTTRILLAD/1work/Python/pydantic_playground/tests/test_FN023.py
 Created: 25 Aug 2021 15:23:07

 DESCRIPTION:

  A suite of unit tests to ensure that the Pydantic model for FN023
  objects validate as expected.

  The script includes a dictionary that representes complete, valid
  data, it then includes a list of required fields that are
  systematically omitted, and finally a list of changes to the
  dictionary of good data that invalidates it in a known way and
  verifies that pydantic raises the expected exception.

 A. Cottrill
=============================================================

"""


import pytest
from pydantic import ValidationError
from datetime import datetime

from creel_portal.data_upload.schemas import FN023


@pytest.fixture()
def data():
    data = {
        "slug": "lha_sc19_002-01-1",
        "season_id": 1,
        "dtp": "2",
        "dtp_nm": "WEEKEND",
        "dow_lst": "17",
    }
    return data


def test_valid_base_data(data):
    """

    Arguments:
    - `data`:
    """

    item = FN023(**data)

    assert item.season_id == data["season_id"]
    assert item.slug == data["slug"]
    assert item.dtp == int(data["dtp"])
    assert item.dtp_nm == data["dtp_nm"]
    assert item.dow_lst == data["dow_lst"]


required_fields = [
    "slug",
    "season_id",
    "dtp",
    "dtp_nm",
    "dow_lst",
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
        FN023(**data)

    msg = "none is not an allowed value"
    assert msg in str(excinfo.value)


error_list = [
    (
        "dtp",
        "A",
        "value is not a valid integer",
    ),
    (
        "dtp",
        "9",
        "value is not a valid enumeration member",
    ),
    (
        "dtp_nm",
        "AB",
        "value is not a valid enumeration member",
    ),
    (
        "dow_lst",
        "00",
        "value is not a valid enumeration member",
    ),
    (
        "dtp_nm",
        "Weekday",
        "value is not a valid enumeration member",
    ),
    (
        "dow_lst",
        "23456",
        "Day type code '2' (WEEKEND) is not consistent with dow list (23456)",
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
        FN023(**data)

    assert msg in str(excinfo.value)


def test_wrong_dtp(data):
    """

    Arguments:
    - `data`:
    """

    msg = "Day type code '1' (WEEKDAY) is not consistent with day type name (WEEKEND)"

    data["dtp"] = "1"
    data["dow_lst"] = "23456"

    with pytest.raises(ValidationError) as excinfo:
        FN023(**data)

    assert msg in str(excinfo.value)
