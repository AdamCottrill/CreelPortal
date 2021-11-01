import django_filters


from .filter_utils import ValueInFilter

from ...models import FN125_Tag

from .FishAttr_Filter import FishAttrFilters


class FN125TagFilter(FishAttrFilters):
    """A filter set class for lamprey data. Inherits all of the filters in
    FishAttrs and add some that are specific to Tag attributes.
    """

    tagid = ValueInFilter(field_name="tagid")
    tagid__like = ValueInFilter(field_name="tagid")
    tagid__not_like = ValueInFilter(field_name="tagid", exclude=True)

    tagdoc = ValueInFilter(field_name="tagdoc")
    tagdoc__like = ValueInFilter(field_name="tagdoc")
    tagdoc__not_like = ValueInFilter(field_name="tagdoc", exclude=True)

    tagstat = ValueInFilter(field_name="tagstat")
    tagstat__not = ValueInFilter(field_name="tagstat", exclude=True)

    # consider splitting up tagdoc into consitiuent fields to make it
    # easier to filter by colour, placement tag type and agency.

    class Meta:
        model = FN125_Tag
        fields = ["tagstat", "tagid", "tagdoc"]
