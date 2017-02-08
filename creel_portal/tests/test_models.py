from django.test import TestCase
from creel_portal.models import *
from creel_portal.tests.factories import *


def test_lake_repr():

    lake = Lake(lake_name = 'Lake Huron', abbrev='HU')
    print(lake)
    assert str(lake) == "<Lake: Lake Huron (HU)>"
