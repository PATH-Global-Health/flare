from django.contrib import admin
from .models import Instance, OrgUnit, DHIS2User, Dataset, DataElement, CategoryCombo, CategoryOptionCombo


class InstanceAdmin(admin.ModelAdmin):
    list_display = ("name", "url",)
    search_fields = ("name", "url", "username")


admin.site.register(Instance, InstanceAdmin)


class OrgUnitAdmin(admin.ModelAdmin):
    list_display = ("name", "org_unit_id", "parent")
    search_fields = ("name", "org_unit_id", "parent")
    list_filter = ("instance__url",)


admin.site.register(OrgUnit, OrgUnitAdmin)


class DHIS2UsersAdmin(admin.ModelAdmin):
    list_display = ("name", "username", "user_id",)  # "org_units")
    search_fields = ("name", "username", "user_id")
    list_filter = ("instance__url",)

    # def org_units(self, instance):
    #     return [ou.name for ou in instance.orgUnits.all()]


admin.site.register(DHIS2User, DHIS2UsersAdmin)


class DatasetsAdmin(admin.ModelAdmin):
    list_display = ("name", "dataset_id",)
    search_fields = ("name", "dataset_id")
    list_filter = ("instance__url",)


admin.site.register(Dataset, DatasetsAdmin)


class DataElementsAdmin(admin.ModelAdmin):
    list_display = ("name", "data_element_id",)
    search_fields = ("name", "data_element_id")
    list_filter = ("instance__url",)


admin.site.register(DataElement, DataElementsAdmin)


class CategoryCombosAdmin(admin.ModelAdmin):
    list_display = ("name", "category_combo_id",)
    search_fields = ("name", "category_combo_id")
    list_filter = ("instance__url",)


admin.site.register(CategoryCombo, CategoryCombosAdmin)


class CategoryOptionCombosAdmin(admin.ModelAdmin):
    list_display = ("name", "category_option_combo_id",)
    search_fields = ("name", "category_option_combo_id")
    list_filter = ("instance__url", "category_combo__name")


admin.site.register(CategoryOptionCombo, CategoryOptionCombosAdmin)
