from django.contrib import admin
from .models import DHIS2Instance, OrgUnit, DHIS2User, Dataset


class DHIS2InstanceAdmin(admin.ModelAdmin):
    list_display = ("name", "url",)
    search_fields = ("name", "url", "username")


admin.site.register(DHIS2Instance, DHIS2InstanceAdmin)


class OrgUnitAdmin(admin.ModelAdmin):
    list_display = ("name", "org_unit_id", "parent")
    search_fields = ("name", "org_unit_id", "parent")
    list_filter = ("instance",)


admin.site.register(OrgUnit, OrgUnitAdmin)


class DHIS2UsersAdmin(admin.ModelAdmin):
    list_display = ("name", "username", "user_id",)  # "org_units")
    search_fields = ("name", "username", "user_id")
    list_filter = ("instance",)

    # def org_units(self, instance):
    #     return [ou.name for ou in instance.orgUnits.all()]


admin.site.register(DHIS2User, DHIS2UsersAdmin)


class DatasetsAdmin(admin.ModelAdmin):
    list_display = ("name", "dataset_id",)
    search_fields = ("name", "dataset_id")
    list_filter = ("instance",)


admin.site.register(Dataset, DatasetsAdmin)
