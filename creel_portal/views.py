from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, DetailView
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.db.models import Q, F
from django.urls import reverse

import json


from creel_portal.models import FN011, FN026, FR713, FR714
from creel_portal.forms import FN026Form, DataUploadForm

from .utils import (
    get_aggregate_catch_estimates,
    get_aggregate_effort_estimates,
    get_catch_totals,
)

from .data_upload.project_upload import process_accdb_upload


class CreelListView(ListView):
    model = FN011
    template_name = "creel_portal/creel_list.html"

    def get_queryset(self, **kwargs):
        queryset = FN011.objects.order_by("lake", "-prj_date0").select_related("lake")
        self.lake = self.kwargs.get("lake")
        self.q = self.request.GET.get("q")

        if self.lake:
            queryset = queryset.filter(lake__lake_name=self.lake)

        if self.q:
            queryset = queryset.filter(
                Q(prj_cd__icontains=self.q) | Q(prj_nm__icontains=self.q)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super(CreelListView, self).get_context_data(**kwargs)
        context["lake"] = self.lake
        context["q"] = self.q
        return context


class CreelDetailView(DetailView):
    """A class based view to provide all of the details assocaited with a
    creel.  In addition to the basic FN011 information, it also
    includes effort and catch estiamtes from the last creel run (if
    one is available.)

    """

    model = FN011
    template_name = "creel_portal/creel_detail.html"
    context_object_name = "creel"

    def get_queryset(self):
        queryset = super(CreelDetailView, self).get_queryset()

        queryset = queryset.select_related("prj_ldr").prefetch_related(
            "seasons",
            "seasons__daytypes",
            "seasons__daytypes__periods",
            "seasons__exception_dates",
            "modes",
            "spatial_strata",
            "creel_run",
        )

        return queryset

    def get_context_data(self, **kwargs):
        """The creel detail page requires a number additional pieces of
        information that are used to populate the map, the tables, and the
        charts."""
        context = super(CreelDetailView, self).get_context_data(**kwargs)

        creel = kwargs.get("object")

        spots = creel.spatial_strata.values("label", "ddlon", "ddlat")
        context["spaces"] = json.dumps(list(spots), cls=DjangoJSONEncoder)

        catch_estimates = get_aggregate_catch_estimates(creel)
        context["catch_estimates"] = catch_estimates

        effort_estimates = get_aggregate_effort_estimates(creel)
        context["effort_estimates"] = effort_estimates

        # these are used by the chart - we might want to move them to
        # the api and load this data via ajax when the page loads.
        catch_totals = get_catch_totals(creel)
        context["catch_totals"] = catch_totals

        return context


def edit_creel_space(request, slug, space):
    """
    Arguments:
    - `request`:
    - `slug`:
    - `space`:
    """

    space = get_object_or_404(FN026, creel__slug=slug, space=space)

    if request.method == "POST":
        form = FN026Form(request.POST, instance=space)
        if form.is_valid():
            form.save()
            return redirect("creel_detail", slug=space.creel.slug)
    else:
        form = FN026Form(instance=space)

    return render(
        request, "creel_portal/edit_creel_space.html", {"form": form, "space": space}
    )


def effort_estimates(request, slug):
    """

    Arguments:
    - `request`:
    """

    creel = get_object_or_404(FN011, slug=slug)

    spots = creel.spatial_strata.values("label", "ddlon", "ddlat")
    spots_json = json.dumps(list(spots), cls=DjangoJSONEncoder)

    return render(
        request,
        "creel_portal/creel_effort_plots.html",
        {"creel": creel, "spaces": spots_json},
    )


def catch_estimates(request, slug):
    """

    Arguments:
    - `request`:
    """

    creel = get_object_or_404(FN011, slug=slug)

    spots = creel.spatial_strata.values("label", "ddlon", "ddlat")
    spots_json = json.dumps(list(spots), cls=DjangoJSONEncoder)

    return render(
        request,
        "creel_portal/creel_catch_plots.html",
        {"creel": creel, "spaces": spots_json},
    )


def effort_estimates_json(request, slug):
    """This is just a temporary function to get the effort estimates for a
    single creel and dump them as json for cross filter to consume. This
    should be reaplaced by a real api endpoint.

    Arguments:
    - `request`:

    """

    creel = FN011.objects.get(slug=slug)
    final_run = creel.final_run.run

    qs = (
        FR713.objects.filter(
            date__isnull=True,
            fr712__rec_tp=2,
            fr712__stratum__creel_run__creel=creel,
            fr712__stratum__creel_run__run=final_run,
        )
        .select_related(
            "fr712__stratum__season",
            "fr712__stratum__season__datetype",
            "fr712__stratum__season__datetype__period",
            "fr712__stratum__mode",
            "fr712__stratum__spatial_strata",
        )
        .annotate(
            season=F("fr712__stratum__season__ssn_des"),
            dtp=F("fr712__stratum__daytype__dtp_nm"),
            period=F("fr712__stratum__period__prd"),
            mode=F("fr712__stratum__mode__mode_des"),
            area=F("fr712__stratum__area__space_des"),
            ddlat=F("fr712__stratum__area__ddlat"),
            ddlon=F("fr712__stratum__area__ddlon"),
        )
        .values(
            "id",
            "effre",
            "effae",
            "effao_s",
            "effro_s",
            "mode",
            "season",
            "dtp",
            "period",
            "area",
            "ddlat",
            "ddlon",
        )
    )

    return JsonResponse(list(qs), safe=False)


def catch_estimates_json(request, slug):
    """This is just a temporary function to get the catch estimates for a
    single creel and dump them as json for cross filter to consume. This
    should be reaplaced by a real api endpoint.

    Arguments:
    - `request`:

    """

    creel = FN011.objects.get(slug=slug)
    final_run = creel.final_run.run

    qs = (
        FR714.objects.filter(
            date__isnull=True,
            fr712__rec_tp=2,
            fr712__stratum__creel_run__creel=creel,
            fr712__stratum__creel_run__run=final_run,
        )
        .select_related(
            "species",
            "fr712__stratum__season",
            "fr712__stratum__season__datetype",
            "fr712__stratum__season__datetype__period",
            "fr712__stratum__mode",
            "fr712__stratum__spatial_strata",
        )
        .annotate(
            species_name=F("species__spc_nmco"),
            season=F("fr712__stratum__season__ssn_des"),
            dtp=F("fr712__stratum__daytype__dtp_nm"),
            period=F("fr712__stratum__period__prd"),
            mode=F("fr712__stratum__mode__mode_des"),
            area=F("fr712__stratum__area__space_des"),
            ddlat=F("fr712__stratum__area__ddlat"),
            ddlon=F("fr712__stratum__area__ddlon"),
        )
        .values(
            "id",
            "species_name",
            "sek",
            "catne",
            "mode",
            "season",
            "dtp",
            "period",
            "area",
            "ddlat",
            "ddlon",
        )
    )

    return JsonResponse(list(qs), safe=False)


# # move this to someplace more appropriate:
def handle_uploaded_file(f):

    upload_dir = settings.UPLOAD_DIR
    fname = os.path.join(upload_dir, f.name)
    if os.path.isfile(fname):
        os.remove(fname)
    with open(fname, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        # now connect to the uploaded file and insert the contents in the appropriate tables...

    data = process_accdb_upload(upload_dir, f.name)
    # delete the file when we are done. if we can.  Not a problem if
    # not, we will periodically nuke the upload directory anyway.
    try:
        os.remove(fname)
    except (PermissionError, OSError):
        pass
    return data


def get_errors(errors):
    """A helper function to extract relavant information from each error
    message so it can be displayed in the template"""
    error_list = []
    for err in errors:
        slug, validation_error = err
        table = validation_error.model.schema().get("title", "")
        for error in validation_error.errors():
            # msg = f"\t{title} => {slug} - {'-'.join(error['loc'])}: {error['msg']}"
            error_dict = {
                "table": table,
                "slug": slug,
                "fields": "-".join(error["loc"]),
                "message": error["msg"],
            }
            error_list.append(error_dict)
    return error_list


@login_required
def project_data_upload(request):
    """A view to process data uploads.  It will be only available to logged in users.

    The uploaded file will be check for validity with cerberus - if it
    looks like it has the correct shape, the data will be passed to a
    stocking event formset, that will allow final editing and form
    validation. Once submitted, the stocking event objects will be
    created.

    Only new stocking model objects can be created for now. An
    extension will be to allow users to bulk edit rrecords - as long
    as the stock_id number can be matched back to the original record.

    """

    if request.method == "POST":

        form = DataUploadForm(request.POST, request.FILES)

        if form.is_valid():

            try:
                data_file = form.cleaned_data["file_upload"]

                if not (
                    data_file.name.endswith(".accdb") or data_file.name.endswith(".db")
                ):
                    msg = "Choosen file is not an Access (*.accdb) file!"
                    messages.error(request, msg)
                    return HttpResponseRedirect(
                        reverse("creel_portal:upload_project_data")
                    )
                # if file is too large, return
                if data_file.multiple_chunks():
                    filesize = data_file.size / (1000 * 1000)
                    msg = (
                        f"The uploaded file is too big ({filesize:.2f} MB). "
                        + "Compact the database before uploading it or considering splitting it into smaller packets."
                    )
                    messages.error(request, msg)
                    return HttpResponseRedirect(
                        reverse("creel_portal:upload_project_data")
                    )

                upload = handle_uploaded_file(data_file)

                if upload["status"] == "insert-error":

                    messages.error(
                        request,
                        "There was a problem inserting the data from: "
                        + data_file.name
                        + ". "
                        + str(upload["errors"]),
                    )
                    return render(request, "creel_portal/project_data_upload.html")

                if upload["status"] == "error":
                    msg = (
                        "There was a problem validating the data from: "
                        + data_file.name
                        + " Please address the issues identified below and try again."
                    )
                    messages.error(request, msg)
                    # pass errors to redirect so that they are available in the response.
                    # return HttpResponseRedirect(reverse("creel_portal:upload_project_data"))
                    error_list = get_errors(upload.get("errors"))
                    return render(
                        request,
                        "creel_portal/project_data_upload.html",
                        {"errors": error_list},
                    )
                else:
                    prj_cds = upload.get("prj_cds")

                    msg = f"Data for {', '.join(prj_cds)} was successfully uploaded!"
                    messages.success(request, message=msg)

                    if len(prj_cds) == 1:
                        slug = prj_cds[0].lower()
                        return HttpResponseRedirect(
                            reverse("creel_portal:creel_detail", kwargs={"slug": slug})
                        )
                    else:
                        return redirect(
                            reverse("creel_portal:creel_list")
                            + f"?prj_cd={','.join(prj_cds)}"
                        )

            except Exception as e:
                messages.error(request, "Unable to upload file. " + repr(e))
                return HttpResponseRedirect(reverse("creel_portal:upload_project_data"))
    else:
        form = DataUploadForm()
    return render(
        request,
        "creel_portal/project_data_upload.html",
        {
            "form": form,
            "upload_template_version": settings.CREEL_UPLOAD_TEMPLATE_VERSION,
        },
    )
