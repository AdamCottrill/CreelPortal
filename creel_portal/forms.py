from django import forms
from django.forms import ModelForm

from creel_portal.models import FN026


class FN026Form(ModelForm):
    """A form to capture attributes of a creel space"""

    class Meta:
        model = FN026
        fields = ["ddlat", "ddlon"]

        widgets = {
            "ddlat": forms.TextInput(attrs={"class": "form-control"}),
            "ddlon": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_ddlon(self):
        """if ddlon is populated it must be between -90 and 90.  If ddlat is
        populated, ddlon is also required."""

        ddlon = self.cleaned_data.get("ddlon")
        if ddlon:
            if ddlon < -180 or ddlon > 180:
                err_msg = "ddlon must be numeric and lie between -180 and 180"
                raise forms.ValidationError(err_msg)
        return ddlon

    def clean_ddlat(self):
        """if ddlat is populated it must be between -90 and 90.  If ddlon is
        populated, ddlat is also required."""

        ddlat = self.cleaned_data.get("ddlat")

        if ddlat:
            if ddlat < -90 or ddlat > 90:
                err_msg = "ddlat must be numeric and lie between -90 and 90"
                raise forms.ValidationError(err_msg)
        return ddlat

    def clean(self):
        """

        Arguments:
        - `self`:
        """

        cleaned_data = self.cleaned_data

        ## DDLAT DDLON
        ddlat = cleaned_data.get("ddlat")
        ddlon = cleaned_data.get("ddlon")

        if ddlat is None and ddlon is not None:
            err_msg = "If ddlon is populated,  ddlat must be populated too"
            raise forms.ValidationError(err_msg)
        if ddlat is not None and ddlon is None:
            err_msg = "If ddlat is populated,  ddlon must be populated too"
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
