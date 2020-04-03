import pytest

from .factories.common_factories import SpeciesFactory
from .factories.fn011_factory import FN011Factory
from .factories.creel_factories import FN111Factory
from .factories.fishnet2_factories import (
    FN121Factory,
    FN123Factory,
    FN125Factory,
    FN125TagFactory,
    FN125LampreyFactory,
    FN127Factory,
)


@pytest.mark.django_db
def test_creel_repr():
    """Verify that a creel is represented by object type, creel name and
    project code."""

    prj_nm = "Test Creel"
    prj_cd = "LHA_SC11_123"

    creel = FN011Factory(prj_nm=prj_nm, prj_cd=prj_cd)

    shouldbe = "<Creel: {} ({})>".format(prj_nm, prj_cd)

    assert str(creel) == shouldbe


@pytest.mark.django_db
def test_sam_repr():
    """The string method of a creel interview should return the object
    type (an interveiw), the sample number and the project code."""

    sam_num = "12345"
    prj_cd = "LHA_SC11_123"
    creel = FN011Factory(prj_cd=prj_cd)
    sama = FN111Factory(creel=creel)
    sam = FN121Factory(sama=sama, sam=sam_num)

    assert str(sam) == "<Interview: {} ({})>".format(sam_num, prj_cd)


@pytest.mark.django_db
def test_catch_count_repr():
    """The string method of a catch count should return the object
    type (a catch count), project code, the sample, species code."""

    spc = "091"
    grp = "XX"
    sam_num = "12345"
    prj_cd = "LHA_SC11_123"
    species = SpeciesFactory(spc=spc)
    creel = FN011Factory(prj_cd=prj_cd)
    sama = FN111Factory(creel=creel)
    interview = FN121Factory(sama=sama, sam=sam_num)
    catch = FN123Factory(interview=interview, species=species, grp=grp)

    assert str(catch) == "<Catch: {}-{}-{}-{}>".format(prj_cd, sam_num, grp, spc)


@pytest.mark.django_db
def test_fish_repr():
    """The string method of fish should return the object
    type (fish), project code, the sample, species code, group code
    and fish number."""

    spc = "091"
    sam_num = "12345"
    prj_cd = "LHA_SC11_123"
    grp = "55"
    fish_num = 321

    species = SpeciesFactory(spc=spc)
    creel = FN011Factory(prj_cd=prj_cd)
    sama = FN111Factory(creel=creel)
    interview = FN121Factory(sama=sama, sam=sam_num)
    catch = FN123Factory(interview=interview, species=species, grp=grp)

    fish = FN125Factory(catch=catch, fish=fish_num)

    shouldbe = "<Fish: {}-{}-{}-{}-{}>".format(prj_cd, sam_num, spc, grp, fish_num)
    assert str(fish) == shouldbe


@pytest.mark.django_db
def test_fish_tag_repr():
    """The string method of fish tag should return the object type (fish
    tag), project code, the sample, species code, group code, fish
    number (the key fields of the parent fish) plus the attributes of
    teh tag: tagid and tagdoc.

    """

    spc = "091"
    sam_num = "12345"
    prj_cd = "LHA_SC11_123"
    grp = "55"
    fish_num = 321

    species = SpeciesFactory(spc=spc)
    creel = FN011Factory(prj_cd=prj_cd)
    sama = FN111Factory(creel=creel)
    interview = FN121Factory(sama=sama, sam=sam_num)
    catch = FN123Factory(interview=interview, species=species, grp=grp)

    fish = FN125Factory(catch=catch, fish=fish_num)

    tagid = "12-34-66A"
    tagdoc = "99999"

    tag = FN125TagFactory(fish=fish, tagid=tagid, tagdoc=tagdoc)

    shouldbe = "{}-{}-{}-{}-{}-{} ({} ({}))".format(
        prj_cd, sam_num, spc, grp, fish_num, tag.fish_tag_id, tagid, tagdoc
    )

    assert str(tag) == shouldbe


@pytest.mark.django_db
def test_fish_lamijc_repr():
    """The string method of a lamprey wound record using the ijc
    convention should return the keys to the parent fish
    project code, the sample, species code, group code, fish number
    plus the attributes the lamprey wound.

    """

    spc = "091"
    sam_num = "12345"
    prj_cd = "LHA_SC11_123"
    grp = "55"
    fish_num = 321

    species = SpeciesFactory(spc=spc)
    creel = FN011Factory(prj_cd=prj_cd)
    sama = FN111Factory(creel=creel)
    interview = FN121Factory(sama=sama, sam=sam_num)
    catch = FN123Factory(interview=interview, species=species, grp=grp)

    fish = FN125Factory(catch=catch, fish=fish_num)

    lamijc = "A230"
    lamprey = FN125LampreyFactory(fish=fish, lamijc=lamijc)

    shouldbe = "{}-{}-{}-{}-{}-{} (lamijc: {})".format(
        prj_cd, sam_num, spc, grp, fish_num, lamprey.lamid, lamijc
    )

    assert str(lamprey) == shouldbe


@pytest.mark.django_db
def test_fish_xlam_repr():
    """The string method of a lamprey wound record using the xlam notation
    should return the keys to the parent fish
    project code, the sample, species code, group code, fish number
    plus the attributes the lamprey wound.

    """

    spc = "091"
    sam_num = "12345"
    prj_cd = "LHA_SC11_123"
    grp = "55"
    fish_num = 321

    species = SpeciesFactory(spc=spc)
    creel = FN011Factory(prj_cd=prj_cd)
    sama = FN111Factory(creel=creel)
    interview = FN121Factory(sama=sama, sam=sam_num)
    catch = FN123Factory(interview=interview, species=species, grp=grp)

    fish = FN125Factory(catch=catch, fish=fish_num)

    xlam = "0101"
    lamprey = FN125LampreyFactory(fish=fish, xlam=xlam)

    shouldbe = "{}-{}-{}-{}-{}-{} (xlam: {})".format(
        prj_cd, sam_num, spc, grp, fish_num, lamprey.lamid, xlam
    )

    assert str(lamprey) == shouldbe


@pytest.mark.django_db
def test_age_estimate_repr():
    """The string method an age estimate should return the object
    type (age estimate), project code, the sample, species code, group code,
    fish number, and ageid."""

    spc = "091"
    sam_num = "12345"
    prj_cd = "LHA_SC11_123"
    grp = "55"
    fish_num = 321
    age_id = 99

    species = SpeciesFactory(spc=spc)
    creel = FN011Factory(prj_cd=prj_cd)
    sama = FN111Factory(creel=creel)
    interview = FN121Factory(sama=sama, sam=sam_num)
    catch = FN123Factory(interview=interview, species=species, grp=grp)
    fish = FN125Factory.build(catch=catch, fish=fish_num)

    age_est = FN127Factory.build(fish=fish, ageid=age_id)
    shouldbe = "<AgeEstimate: {}-{}-{}-{}-{}-{}>".format(
        prj_cd, sam_num, spc, grp, fish_num, age_id
    )
    assert str(age_est) == shouldbe
