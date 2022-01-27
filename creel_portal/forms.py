from django import forms
from django.forms import ModelForm

from creel_portal.models import FN026


class FN026Form(ModelForm):
    """A form to capture attributes of a creel space"""

    class Meta:
        model = FN026
        fields = ["dd_lat", "dd_lon"]

        widgets = {
            "dd_lat": forms.TextInput(attrs={"class": "form-control"}),
            "dd_lon": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_dd_lon(self):
        """if dd_lon is populated it must be between -90 and 90.  If dd_lat is
        populated, dd_lon is also required."""

        dd_lon = self.cleaned_data.get("dd_lon")
        if dd_lon:
            if dd_lon < -180 or dd_lon > 180:
                err_msg = "dd_lon must be numeric and lie between -180 and 180"
                raise forms.ValidationError(err_msg)
        return dd_lon

    def clean_dd_lat(self):
        """if dd_lat is populated it must be between -90 and 90.  If dd_lon is
        populated, dd_lat is also required."""

        dd_lat = self.cleaned_data.get("dd_lat")

        if dd_lat:
            if dd_lat < -90 or dd_lat > 90:
                err_msg = "dd_lat must be numeric and lie between -90 and 90"
                raise forms.ValidationError(err_msg)
        return dd_lat

    def clean(self):
        """

        Arguments:
        - `self`:
        """

        cleaned_data = self.cleaned_data

        ## DD_LAT DD_LON
        dd_lat = cleaned_data.get("dd_lat")
        dd_lon = cleaned_data.get("dd_lon")

        if dd_lat is None and dd_lon is not None:
            err_msg = "If dd_lon is populated,  dd_lat must be populated too"
            raise forms.ValidationError(err_msg)
        if dd_lat is not None and dd_lon is None:
            err_msg = "If dd_lat is populated,  dd_lon must be populated too"
            raise forms.ValidationError(err_msg)

        return cleaned_data


class DataUploadForm(forms.Form):
    """A simple little form for uploading our tempalte databases one at a time."""

    file_upload = forms.FileField(label="Project Data", required=True)

    def __init__(self, *args, **kwargs):

        super(DataUploadForm, self).__init__(*args, **kwargs)
        self.fields["file_upload"].widget.attrs["size"] = "40"
        self.fields["file_upload"].widget.attrs["class"] = "form-control"
        self.fields["file_upload"].widget.attrs["accept"] = ".accdb"
        self.fields["file_upload"].widget.attrs["id"] = "data_file"

        self.fields["file_upload"].widget.attrs["name"] = "data_file"
