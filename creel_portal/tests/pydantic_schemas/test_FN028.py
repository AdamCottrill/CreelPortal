"""=============================================================
 c:/Users/COTTRILLAD/1work/Python/pydantic_playground/tests/test_FN028.py
 Created: 25 Aug 2021 15:23:07

 DESCRIPTION:

  A suite of unit tests to ensure that the Pydantic model for FN028
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
from datetime import time

from creel_portal.data_upload.schemas import FN028


@pytest.fixture()
def data():
    data = {
        "slug": "lha_ia19_002-A1",
        "gear_id": 1,
        "creel_id": 1,
        "mode": "A1",
        "mode_des": "the lake",
        "atyunit": 1,
        "itvunit": 1,
        "chkflag": 0,
    }
    return data


def test_valid_data(data):
    """

    Arguments:
    - `data`:
    """

    item = FN028(**data)

    assert item.creel_id == data["creel_id"]
    assert item.slug == data["slug"]
    assert item.mode == data["mode"].strip().title()
    assert item.mode_des == data["mode_des"].strip().title()


required_fields = [
    "slug",
    "creel_id",
    "mode",
    "atyunit",
    "itvunit",
    "chkflag",
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
        FN028(**data)
    msg = "none is not an allowed value"
    assert msg in str(excinfo.value)


optional_fields = [
    "mode_des",
]


@pytest.mark.parametrize("fld", optional_fields)
def test_optional_fields(data, fld):
    """Verify that the FN028 item is created without error if an optional field is omitted

    Arguments:
    - `data`:

    """
    data[fld] = None
    item = FN028(**data)
    assert item.creel_id == data["creel_id"]


mode_list = [
    # field, input, output
    ("mode", "aa", "AA"),
    ("mode", "a1", "A1"),
    ("mode", "AA", "AA"),
    ("mode", "A1", "A1"),
    ("mode", "00", "00"),
    (
        "mode_des",
        "open water angling",
        "Open Water Angling",
    ),
    (
        "mode_des",
        "OPEN WATER ANGLING",
        "Open Water Angling",
    ),
    (
        "mode_des",
        "Open Water Angling",
        "Open Water Angling",
    ),
    (
        "mode_des",
        None,
        "Not Specified",
    ),
]


@pytest.mark.parametrize("fld,value_in,value_out", mode_list)
def test_valid_alternatives(data, fld, value_in, value_out):
    """When the pydanic model is created, it should transform some fo the
    fields.  Mode should be a two letter code made from uppercase
    letters or digits.  The pydantic model should convert any letters
    to uppercase automatically. Uppercase letters and any numbers
    should be returned unchanged.  mode_des should be trimmed of any
    white mode and converted to upper case.

    Arguments:
    - `data`:

    """
    data[fld] = value_in
    item = FN028(**data)
    item_dict = item.dict()
    assert item_dict[fld] == value_out


error_list = [
    (
        "mode",
        "AA1",
        "ensure this value has at most 2 characters",
    ),
    (
        "mode",
        "A*",
        'string does not match regex "^([A-Z0-9]{2})$"',
    ),
    (
        "itvunit",
        99,
        "value is not a valid enumeration member;",
    ),
    (
        "atyunit",
        99,
        "value is not a valid enumeration member;",
    ),
    (
        "chkflag",
        99,
        "value is not a valid enumeration member;",
    ),
    (
        "atyunit",
        2,
        "If ATYUNIT=2, then ITVUNIT must also equal 2.",
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
        FN028(**data)

    assert msg in str(excinfo.value)
