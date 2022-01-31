"""=============================================================
 c:/Users/COTTRILLAD/1work/Python/pydantic_playground/tests/test_FN024.py
 Created: 25 Aug 2021 15:23:07

 DESCRIPTION:

  A suite of unit tests to ensure that the Pydantic model for FN024
  objects validate as expected.

  The script includes a dictionary that representes complete, valid
  data, it then includes a list of required fields that are
  systematically omitted, and finally a list of changes to the
  dictionary of good data that invalidates it in a known way and
  verifies that pydantic raises the expected exception.

 A. Cottrill
=============================================================

"""

from datetime import time
import pytest
from pydantic import ValidationError
from datetime import datetime

from creel_portal.data_upload.schemas import FN024


@pytest.fixture()
def data():
    data = {
        "slug": "lha_sc19_002-01-1-1",
        "daytype_id": 1,
        "prd": "1",
        "prdtm0": time(8, 0),
        "prdtm1": time(12, 0),
        "prd_dur": 4,
    }
    return data


def test_valid_base_data(data):
    """

    Arguments:
    - `data`:
    """

    item = FN024(**data)

    assert item.daytype_id == data["daytype_id"]
    assert item.slug == data["slug"]
    assert item.prd == data["prd"]
    assert item.prdtm0 == data["prdtm0"]
    assert item.prdtm1 == data["prdtm1"]
    assert item.prd_dur == data["prd_dur"]


required_fields = ["slug", "daytype_id", "prd", "prdtm0", "prdtm1", "prd_dur"]


@pytest.mark.parametrize("fld", required_fields)
def test_required_fields(data, fld):
    """Verify that the required fields without custome error message
    raise the default messge if they are not provided.


    Arguments:
    - `data`:

    """

    data[fld] = None

    with pytest.raises(ValidationError) as excinfo:
        FN024(**data)

    msg = "none is not an allowed value"
    assert msg in str(excinfo.value)


error_list = [
    (
        "prd",
        "FOO",
        "ensure this value has at most 1 characters",
    ),
    (
        "prd",
        "*",
        "string does not match regex",
    ),
    (
        "prd_dur",
        "-1.2",
        "ensure this value is greater than or equal to 0",
    ),
    (
        "prdtm0",
        "24:00",
        "invalid time format",
    ),
    (
        "prdtm0",
        "16:00",
        "Period end time (prdtm1=12:00) occurs before start time(prdtm0=16:00)",
    ),
    (
        "prd_dur",
        "3.5",
        (
            "Period duration (prd_dur=3.5) is not consistent with period start "
            + "and end (08:00, 12:00, delta=4.0)."
        ),
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
        FN024(**data)

    assert msg in str(excinfo.value)
