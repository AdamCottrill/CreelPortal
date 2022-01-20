from datetime import time
import pytest
from pydantic import ValidationError

from creel_portal.data_upload.schemas import FN112


@pytest.fixture()
def data():
    data = {
        "slug": "lha_ia19_002-1-001-091-00-50",
        "sama_id": 1,
        "atytm0": time(8, 0),
        "atytm1": time(8, 15),
        "atydur": 0.25,
        "atycnt": 10,
        "itvcnt": 8,
        "chkcnt": 2,
    }
    return data


def test_valid_data(data):
    """

    Arguments:
    - `data`:
    """

    item = FN112(**data)

    assert item.sama_id == data["sama_id"]
    assert item.slug == data["slug"]


required_fields = [
    "slug",
    "sama_id",
    "atytm0",
    "atytm1",
    "atydur",
    "atycnt",
    "itvcnt",
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
        FN112(**data)
    msg = "none is not an allowed value"
    assert msg in str(excinfo.value)


#
fields_defaults = [("atycnt", 0), ("itvcnt", 0), ("chkcnt", 0)]


@pytest.mark.parametrize("fld,value", fields_defaults)
def test_defaults_data(data, fld, value):
    """

    Arguments:
    - `data`:
    """

    data[fld] = value
    item = FN112(**data)
    item_dict = dict(item)
    assert item_dict[fld] == value


error_list = [
    (
        "atycnt",
        -4,
        "ensure this value is greater than or equal to 0",
    ),
    (
        "itvcnt",
        -4,
        "ensure this value is greater than or equal to 0",
    ),
    (
        "chkcnt",
        -1,
        "ensure this value is greater than or equal to 0",
    ),
    (
        "atydur",
        -1.2,
        "ensure this value is greater than or equal to 0",
    ),
    (
        "atytm0",
        "foobar",
        "invalid time format",
    ),
    (
        "atytm0",
        "-9:00",
        "invalid time format",
    ),
    (
        "atytm0",
        "24:00",
        "invalid time format",
    ),
    (
        "atytm0",
        "24:11",
        "invalid time format",
    ),
    (
        "atytm1",
        "foobar",
        "invalid time format",
    ),
    (
        "atytm1",
        "-9:00",
        "invalid time format",
    ),
    (
        "atytm1",
        "24:00",
        "invalid time format",
    ),
    (
        "atytm1",
        "24:11",
        "invalid time format",
    ),
    (
        "atytm0",
        "10:00",
        "Activity Count end time (atytm1=08:15) occurs before start time(atytm0=10:00)",
    ),
    (
        "atydur",
        "0.75",
        (
            "Activity duration (atydur=0.75) is not consistent with start "
            + "and end times(08:00, 08:15, delta=0.25)."
        ),
    ),
]


# check bad times


@pytest.mark.parametrize("fld,value,msg", error_list)
def test_invalid_data(data, fld, value, msg):
    """

    Arguments:
    - `data`:
    """

    data[fld] = value
    with pytest.raises(ValidationError) as excinfo:
        FN112(**data)

    assert msg in str(excinfo.value)
