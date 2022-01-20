"""=============================================================
 c:/Users/COTTRILLAD/1work/Python/pydantic_playground/tests/test_FN025.py
 Created: 25 Aug 2021 15:23:07

 DESCRIPTION:

  A suite of unit tests to ensure that the Pydantic model for FN025
  objects validate as expected.

  The script includes a dictionary that representes complete, valid
  data, it then includes a list of required fields that are
  systematically omitted, and finally a list of changes to the
  dictionary of good data that invalidates it in a known way and
  verifies that pydantic raises the expected exception.

 A. Cottrill
=============================================================

"""

from datetime import date
import pytest
from pydantic import ValidationError
from datetime import datetime

from creel_portal.data_upload.schemas import FN025


@pytest.fixture()
def data():
    data = {"slug": "lha_sc19_002-01-1-1", "season_id": 1, "date": datetime(2019, 8, 3)}
    return data


def test_valid_base_data(data):
    """

    Arguments:
    - `data`:
    """

    item = FN025(**data)

    assert item.season_id == data["season_id"]
    assert item.slug == data["slug"]
    assert item.date == data["date"].date()


required_fields = ["slug", "season_id", "date"]


@pytest.mark.parametrize("fld", required_fields)
def test_required_fields(data, fld):
    """Verify that the required fields without custome error message
    raise the default messge if they are not provided.


    Arguments:
    - `data`:

    """

    data[fld] = None

    with pytest.raises(ValidationError) as excinfo:
        FN025(**data)

    msg = "none is not an allowed value"
    assert msg in str(excinfo.value)


error_list = [
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
]


@pytest.mark.parametrize("fld,value,msg", error_list)
def test_invalid_data(data, fld, value, msg):
    """
    Arguments:
    - `data`:
    """

    data[fld] = value

    with pytest.raises(ValidationError) as excinfo:
        FN025(**data)

    assert msg in str(excinfo.value)
