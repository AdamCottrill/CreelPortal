"""=============================================================
 c:/Users/COTTRILLAD/1work/Python/pydantic_playground/tests/test_FN126.py
 Created: 26 Aug 2021 16:43:50

 DESCRIPTION:

  A suite of unit tests to ensure that the Pydantic model for FN126
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

from creel_portal.data_upload.schemas import FN126


@pytest.fixture()
def data():
    data = {
        "slug": "lha_ia19_002-1-001-091-00-1",
        "fish_id": 1,
        "food": 1,
        "taxon": "F121",
        "fdcnt": 12,
        "fdmes": "L",
        "fdval": None,
        "lf": None,
        "comment6": "A diet item.",
    }
    return data


def test_valid_data(data):
    """

    Arguments:
    - `data`:
    """

    item = FN126(**data)

    assert item.fish_id == data["fish_id"]
    assert item.slug == data["slug"]


required_fields = ["slug", "fish_id", "food", "taxon", "fdcnt"]


@pytest.mark.parametrize("fld", required_fields)
def test_required_fields(data, fld):
    """Verify that the required fields without custome error message
    raise the default messge if they are not provided.


    Arguments:
    - `data`:

    """

    data[fld] = None

    with pytest.raises(ValidationError) as excinfo:
        FN126(**data)
    msg = "none is not an allowed value"
    assert msg in str(excinfo.value)


optional_fields = ["fdmes", "fdval", "lf", "comment6"]


@pytest.mark.parametrize("fld", optional_fields)
def test_optional_fields(data, fld):
    """Verify that the FN126 item is created without error if an optional field is omitted

    Arguments:
    - `data`:

    """
    data[fld] = None
    item = FN126(**data)
    assert item.slug == data["slug"]


mode_list = [
    # field, input, output
    ("fdval", "", None),
    ("lf", "", None),
]


@pytest.mark.parametrize("fld,value_in,value_out", mode_list)
def test_valid_alternatives(data, fld, value_in, value_out):
    """When the pydanic model is created, it should transform some fo the
    fields.  GRP should be a two letter code made from uppercase
    letters or digits.  The pydantic model should convert any letters
    to uppercase automatically. Uppercase letters and any numbers
    should be returned unchanged.

    Arguments:
    - `data`:

    """
    data[fld] = value_in
    item = FN126(**data)
    item_dict = item.dict()
    assert item_dict[fld] == value_out


error_list = [
    (
        "fdcnt",
        -4,
        "ensure this value is greater than or equal to 0",
    ),
    (
        "lf",
        -4,
        "ensure this value is greater than 0",
    ),
    (
        "fdval",
        -4.0,
        "ensure this value is greater than 0",
    ),
    (
        "fdmes",
        "foo",
        "value is not a valid enumeration member;",
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
        FN126(**data)

    assert msg in str(excinfo.value)
