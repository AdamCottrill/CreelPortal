from django.contrib import admin

from .models.fishnet2 import FN011, FN121, FN123, FN125

from .models.creel_tables import FN022, FN023, FN024, FN025, FN026, FN028, FN111, FN112

# Register your models here.

# f&flter - project lead, lake, prj_cd, prj_nm, creel type, year
# search_ prj_nm, comment0


class FN011Admin(admin.ModelAdmin):

    date_hierachy = "prj_date0"
    list_display = [
        "prj_cd",
        "get_prj_nm",
        "get_prj_ldr",
        "get_lake_name",
        "contmeth",
        "year",
    ]

    list_filter = ["lake__lake_name", "contmeth", "year", "prj_ldr"]

    search_fields = ["prj_cd", "prj_nm"]
    ordering = ["-year"]

    list_select_related = ["lake", "prj_ldr"]

    def get_lake_name(self, object):
        return object.lake.lake_name

    get_lake_name.short_description = "Lake"

    def get_prj_nm(self, object):
        return object.prj_nm.title()

    get_prj_nm.short_description = "PRJ_NM"

    def get_prj_ldr(self, object):
        return "{} {}".format(object.prj_ldr.first_name, object.prj_ldr.first_name)

    get_prj_nm.short_description = "PRJ_LDR"


admin.site.register(FN011, FN011Admin)


class FN022Admin(admin.ModelAdmin):
    list_display = [
        "get_prj_cd",
        "get_season",
        "ssn_date0",
        "ssn_date1",
        "get_lake_name",
    ]

    list_filter = [
        "creel__lake__lake_name",
        # "creel_type"
    ]

    search_fields = ["creel__prj_cd", "creel__prj_nm"]

    ordering = ["creel__prj_cd", "ssn"]

    list_select_related = ["creel", "creel__lake"]

    def get_season(self, object):
        return "{} ({})".format(object.ssn_des.title(), object.ssn)

    get_season.short_description = "Season"

    def get_lake_name(self, object):
        return object.creel.lake.lake_name

    get_lake_name.short_description = "Lake"

    def get_prj_cd(self, object):
        return object.creel.prj_cd

    get_prj_cd.short_description = "PRJ_CD"


admin.site.register(FN022, FN022Admin)


class FN023Admin(admin.ModelAdmin):
    list_display = ["get_prj_cd", "get_season", "get_lake_name", "get_daytype"]

    list_filter = [
        "season__creel__lake__lake_name",
        # "creel_type"
    ]

    search_fields = ["season__creel__prj_cd", "season__creel__prj_nm"]

    ordering = ["season__creel__prj_cd", "season__ssn", "dtp"]

    list_select_related = ["season", "season__creel", "season__creel__lake"]

    def get_daytype(self, object):
        return "{} ({})".format(object.dtp_nm.title(), object.dtp)

    get_daytype.short_description = "Day Type"

    def get_season(self, object):
        return "{} ({})".format(object.season.ssn_des.title(), object.season.ssn)

    get_season.short_description = "Season"

    def get_lake_name(self, object):
        return object.season.creel.lake.lake_name

    get_lake_name.short_description = "Lake"

    def get_prj_cd(self, object):
        return object.season.creel.prj_cd

    get_prj_cd.short_description = "PRJ_CD"

    def get_form(self, request, obj=None, **kwargs):
        form = super(FN023Admin, self).get_form(request, obj, **kwargs)
        form.base_fields["season"].queryset = FN022.objects.filter(
            creel=obj.season.creel
        )
        return form


#    def render_change_form(self, request, context, *args, **kwargs):
#        context["adminform"].form.fields["season"].queryset = FN022.objects.all()[:10]
#        return super(FN023Admin, self).render_change_form(
#            request, context, *args, **kwargs
#        )


admin.site.register(FN023, FN023Admin)


class FN024Admin(admin.ModelAdmin):

    list_display = [
        "get_prj_cd",
        "get_season",
        "get_daytype",
        "prd",
        "prdtm0",
        "prdtm1",
        "prd_dur",
    ]

    list_filter = [
        "daytype__season__creel__lake__lake_name",
        # "creel_type"
    ]

    search_fields = ["daytype__season__creel__prj_cd", "daytype__season__creel__prj_nm"]

    list_select_related = [
        "daytype__season",
        "daytype__season__creel",
        "daytype__season__creel__lake",
    ]

    ordering = [
        "daytype__season__creel__prj_cd",
        "daytype__season__ssn",
        "daytype",
        "prdtm0",
    ]

    def get_daytype(self, object):
        return "{} ({})".format(object.daytype.dtp_nm.title(), object.daytype.dtp)

    get_daytype.short_description = "Day Type"

    def get_season(self, object):
        return "{} ({})".format(
            object.daytype.season.ssn_des.title(), object.daytype.season.ssn
        )

    get_season.short_description = "Season"

    def get_prj_cd(self, object):
        return object.daytype.season.creel.prj_cd

    get_prj_cd.short_description = "PRJ_CD"

    def get_form(self, request, obj=None, **kwargs):
        form = super(FN024Admin, self).get_form(request, obj, **kwargs)
        form.base_fields["daytype"].queryset = FN023.objects.filter(
            season=obj.daytype.season
        )
        return form


admin.site.register(FN024, FN024Admin)


class FN025Admin(admin.ModelAdmin):

    list_display = [
        "get_prj_cd",
        "get_season",
        "get_lake_name",
        "date",
        "dtp1",
        "description"
        # "get_daytype"
    ]

    list_filter = [
        "season__creel__lake__lake_name",
        # "creel_type"
    ]

    list_select_related = ["season__creel", "season__creel__lake"]

    search_fields = ["season__creel__prj_cd", "season__creel__prj_nm"]

    ordering = ["season__creel__prj_cd", "season__ssn"]

    #    def get_daytype(self, object):
    #        return "{} ({})".format(object.dtp_nm.title(), object.dtp)
    #
    #    get_daytype.short_description = "Day Type"

    def get_season(self, object):
        return "{} ({})".format(object.season.ssn_des.title(), object.season.ssn)

    get_season.short_description = "Season"

    def get_lake_name(self, object):
        return object.season.creel.lake.lake_name

    get_lake_name.short_description = "Lake"

    def get_prj_cd(self, object):
        return object.season.creel.prj_cd

    get_prj_cd.short_description = "PRJ_CD"

    def get_form(self, request, obj=None, **kwargs):
        form = super(FN025Admin, self).get_form(request, obj, **kwargs)
        form.base_fields["season"].queryset = FN022.objects.filter(
            creel=obj.season.creel
        )
        return form


admin.site.register(FN025, FN025Admin)


class FN026Admin(admin.ModelAdmin):

    list_display = ["get_prj_cd", "get_prj_nm", "get_lake_name", "get_space", "label"]

    list_filter = [
        "creel__lake__lake_name",
        # "creel_type"
    ]

    list_select_related = ["creel", "creel__lake"]

    search_fields = ["creel__prj_cd", "creel__prj_nm"]

    ordering = ["creel__prj_cd", "space"]

    def get_space(self, object):
        return "{} ({})".format(object.space_des.title(), object.space)

    get_space.short_description = "Lake"

    def get_lake_name(self, object):
        return object.creel.lake.lake_name

    get_lake_name.short_description = "Lake"

    def get_prj_cd(self, object):
        return object.creel.prj_cd

    get_prj_cd.short_description = "PRJ_CD"

    def get_prj_nm(self, object):
        return object.creel.prj_nm.title()

    get_prj_nm.short_description = "PRJ_NM"


admin.site.register(FN026, FN026Admin)


class FN028Admin(admin.ModelAdmin):

    list_display = ["get_prj_cd", "get_prj_nm", "get_mode"]

    list_filter = [
        "creel__lake__lake_name",
        # "creel_type"
    ]

    search_fields = ["creel__prj_cd", "creel__prj_nm"]

    ordering = ["creel__prj_cd", "mode"]

    list_select_related = ["creel", "creel__lake"]

    def get_mode(self, object):
        return "{} ({})".format(object.mode_des.title(), object.mode)

    get_mode.short_description = "Mode"

    def get_prj_cd(self, object):
        return object.creel.prj_cd

    get_prj_cd.short_description = "PRJ_CD"

    def get_prj_nm(self, object):
        return object.creel.prj_nm.title()

    get_prj_nm.short_description = "PRJ_NM"


admin.site.register(FN028, FN028Admin)


class FN111Admin(admin.ModelAdmin):

    list_display = [
        "get_prj_cd",
        "sama",
        "date",
        "samtm0",
        "get_prj_nm",
        "get_season",
        "get_daytype",
        "get_period",
        "get_area",
        "get_mode",
    ]

    list_filter = [
        "creel__lake__lake_name",
        # "creel_type"
    ]

    search_fields = ["creel__prj_cd", "creel__prj_nm"]

    ordering = ["creel__prj_cd", "sama"]

    list_select_related = ["creel", "period", "season", "daytype", "area", "mode"]

    def get_prj_cd(self, object):
        return object.creel.prj_cd

    get_prj_cd.short_description = "PRJ_CD"

    def get_prj_nm(self, object):
        return object.creel.prj_nm.title()

    get_prj_nm.short_description = "PRJ_NM"

    def get_season(self, object):
        return "{} ({})".format(object.season.ssn_des.title(), object.season.ssn)

    get_season.short_description = "Season"

    def get_period(self, object):
        start = object.period.prdtm0.strftime("%H:%M")
        end = object.period.prdtm1.strftime("%H:%M")
        return "{} ({}-{})".format(object.period.prd, start, end)

    get_period.short_description = "Period"

    def get_daytype(self, object):
        return "{} ({})".format(object.daytype.dtp_nm.title(), object.daytype.dtp)

    get_daytype.short_description = "Day Type"

    def get_area(self, object):
        return "{} ({})".format(object.area.space_des.title(), object.area.space)

    get_area.short_description = "Space"

    def get_mode(self, object):
        return "{} ({})".format(object.mode.mode_des.title(), object.mode.mode)

    get_mode.short_description = "Mode"


admin.site.register(FN111, FN111Admin)


class FN112Admin(admin.ModelAdmin):

    list_display = [
        "get_prj_cd",
        "get_sama",
        "get_date",
        "get_samtm0",
        "get_season",
        "get_daytype",
        "get_period",
        "get_area",
        "get_mode",
        "atytm0",
        "atycnt",
        "chkcnt",
        "itvcnt",
    ]

    list_filter = [
        "sama__creel__lake__lake_name",
        # "creel_type"
    ]

    search_fields = ["sama__creel__prj_cd", "sama__creel__prj_nm"]

    ordering = ["sama__creel__prj_cd", "sama__sama"]

    list_select_related = [
        "sama",
        "sama__creel",
        "sama__creel__lake",
        "sama__area",
        "sama__season",
        "sama__period",
        "sama__daytype",
        "sama__mode",
    ]

    def get_prj_cd(self, object):
        return object.sama.creel.prj_cd

    get_prj_cd.short_description = "PRJ_CD"

    def get_sama(self, object):
        return object.sama.sama

    get_sama.short_description = "SAMA"

    def get_date(self, object):
        return object.sama.date

    get_date.short_description = "Date"

    def get_samtm0(self, object):

        return object.sama.samtm0.strftime("%H:%M")

    get_samtm0.short_description = "SAMTM0"

    def get_season(self, object):
        return "{} ({})".format(
            object.sama.season.ssn_des.title(), object.sama.season.ssn
        )

    get_season.short_description = "Season"

    def get_period(self, object):
        start = object.sama.period.prdtm0.strftime("%H:%M")
        end = object.sama.period.prdtm1.strftime("%H:%M")
        return "{} ({}-{})".format(object.sama.period.prd, start, end)

    get_period.short_description = "Period"

    def get_daytype(self, object):
        return "{} ({})".format(
            object.sama.daytype.dtp_nm.title(), object.sama.daytype.dtp
        )

    get_daytype.short_description = "Day Type"

    def get_area(self, object):
        return "{} ({})".format(
            object.sama.area.space_des.title(), object.sama.area.space
        )

    get_area.short_description = "Space"

    def get_mode(self, object):
        return "{} ({})".format(
            object.sama.mode.mode_des.title(), object.sama.mode.mode
        )

    get_mode.short_description = "Mode"


admin.site.register(FN112, FN112Admin)


class FN121Admin(admin.ModelAdmin):
    list_display = [
        "sam",
        "get_prj_cd",
        "get_sama",
        "get_date",
        "get_itvtm0",
        "get_season",
        "get_daytype",
        "get_period",
        "get_area",
        "get_mode",
    ]

    search_fields = ["sama__creel__prj_cd", "sama__creel__prj_nm"]

    ordering = ["sama__creel__prj_cd", "sama__sama"]

    list_filter = [
        "sama__creel__lake__lake_name",
        # "creel_type"
    ]

    list_select_related = [
        "sama",
        "sama__creel",
        "sama__creel__lake",
        "sama__area",
        "sama__season",
        "sama__period",
        "sama__daytype",
        "sama__mode",
    ]

    # limit the choice of creel log to those in the same creel:
    def get_form(self, request, obj=None, **kwargs):
        form = super(FN121Admin, self).get_form(request, obj, **kwargs)
        form.base_fields["sama"].queryset = FN111.objects.filter(
            creel=obj.sama.creel
        ).select_related("creel")
        return form

    def get_prj_cd(self, object):
        return object.sama.creel.prj_cd

    get_prj_cd.short_description = "PRJ_CD"

    def get_sama(self, object):
        return object.sama.sama

    get_sama.short_description = "SAMA"

    def get_date(self, object):
        return object.date

    get_date.short_description = "Date"

    def get_itvtm0(self, object):

        return object.itvtm0.strftime("%H:%M")

    get_itvtm0.short_description = "Date"

    def get_season(self, object):
        return "{} ({})".format(
            object.sama.season.ssn_des.title(), object.sama.season.ssn
        )

    get_season.short_description = "Season"

    def get_period(self, object):
        start = object.sama.period.prdtm0.strftime("%H:%M")
        end = object.sama.period.prdtm1.strftime("%H:%M")
        return "{} ({}-{})".format(object.sama.period.prd, start, end)

    get_period.short_description = "Period"

    def get_daytype(self, object):
        return "{} ({})".format(
            object.sama.daytype.dtp_nm.title(), object.sama.daytype.dtp
        )

    get_daytype.short_description = "Day Type"

    def get_area(self, object):
        return "{} ({})".format(
            object.sama.area.space_des.title(), object.sama.area.space
        )

    get_area.short_description = "Space"

    def get_mode(self, object):
        return "{} ({})".format(
            object.sama.mode.mode_des.title(), object.sama.mode.mode
        )

    get_mode.short_description = "Mode"


admin.site.register(FN121, FN121Admin)


class FN123Admin(admin.ModelAdmin):

    list_display = [
        "get_prj_cd",
        "get_sam",
        "get_species",
        "sek",
        "hvscnt",
        "rlscnt",
        "mescnt",
        "meswt",
    ]

    search_fields = ["interview__sama__creel__prj_cd", "interview__sama__creel__prj_nm"]

    ordering = ["interview__sama__creel__prj_cd", "interview__sam"]

    list_filter = [
        "interview__sama__creel__lake__lake_name",
        "sek",
        # "creel_type"
    ]

    list_select_related = [
        "interview",
        "interview__sama__creel",
        "interview__sama__creel__lake",
        "species",
    ]

    def get_prj_cd(self, object):
        return object.interview.sama.creel.prj_cd

    get_prj_cd.short_description = "PRJ_CD"

    def get_sam(self, object):
        return object.interview.sam

    get_sam.short_description = "SAM"

    def get_species(self, object):
        return "{} ({})".format(
            object.species.common_name.title(), object.species.species_code
        )

    get_species.short_description = "Species"


admin.site.register(FN123, FN123Admin)


class FN125Admin(admin.ModelAdmin):
    pass


admin.site.register(FN125, FN125Admin)
