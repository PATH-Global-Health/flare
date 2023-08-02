from django.contrib import admin
from .models import Instance, OrgUnit, DHIS2User, Dataset, DataElement, CategoryCombo, CategoryOptionCombo, \
    Section, UserGroup, DataValueSet, DataValue, DatasetDataElement, DataElementGroup, DataElementGroupSet, \
    DataElementGroupGroupSet


class InstanceAdmin(admin.ModelAdmin):
    list_display = ("name", "url",)
    search_fields = ("name", "url", "username")


admin.site.register(Instance, InstanceAdmin)


class OrgUnitAdmin(admin.ModelAdmin):
    list_display = ("name", "org_unit_id", "parent")
    search_fields = ("name", "org_unit_id", "parent")
    list_filter = ("instance__url",)


admin.site.register(OrgUnit, OrgUnitAdmin)


class UserGroupsAdmin(admin.ModelAdmin):
    list_display = ("name", "group_id")
    search_fields = ("name", "group_id")
    list_filter = ("instance__url",)


admin.site.register(UserGroup, UserGroupsAdmin)


class DHIS2UsersAdmin(admin.ModelAdmin):
    list_display = ("name", "username", "user_id", "passcode")  # "org_units")
    search_fields = ("name", "username", "user_id", "passcode")
    list_filter = ("instance__url", "group__name")

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


class DataElementGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "data_element_group_id",)
    search_fields = ("name", "data_element_group_id")
    list_filter = ("instance__url",)


admin.site.register(DataElementGroup, DataElementGroupAdmin)


class DataElementGroupSetAdmin(admin.ModelAdmin):
    list_display = ("name", "data_element_groupset_id",)
    search_fields = ("name", "data_element_groupset_id")
    list_filter = ("instance__url",)


admin.site.register(DataElementGroupSet, DataElementGroupSetAdmin)


class DataElementGroupGroupSetAdmin(admin.ModelAdmin):
    list_display = ("data_element_group",
                    "data_element_groupset", "sort_order")
    search_fields = ("data_element_group__name", "data_element_groupset__name")
    list_filter = ("instance__url", "data_element_groupset__name")


admin.site.register(DataElementGroupGroupSet, DataElementGroupGroupSetAdmin)


class CategoryCombosAdmin(admin.ModelAdmin):
    list_display = ("name", "category_combo_id",)
    search_fields = ("name", "category_combo_id")
    list_filter = ("instance__url",)


admin.site.register(CategoryCombo, CategoryCombosAdmin)


class CategoryOptionCombosAdmin(admin.ModelAdmin):
    list_display = ("name", "sort_order", "category_option_combo_id",)
    search_fields = ("name", "category_option_combo_id")
    list_filter = ("instance__url", "category_combo__name")


admin.site.register(CategoryOptionCombo, CategoryOptionCombosAdmin)


class SectionsAdmin(admin.ModelAdmin):
    list_display = ("name", "section_id", "sort_order")
    search_fields = ("name", "section_id")
    list_filter = ("instance__url", "dataset__name")


admin.site.register(Section, SectionsAdmin)


class DataValueSetAdmin(admin.ModelAdmin):
    list_display = ("data_set", "org_unit", "user", "period", "phone_number", "status", "mark_as_complete",
                    "created_at", "updated_at")
    search_fields = ("data_set__name", "org_unit__name",
                     "user__name", "period", "phone_number")
    list_filter = ("status", "data_set__name", "mark_as_complete")


admin.site.register(DataValueSet, DataValueSetAdmin)


class DataValueAdmin(admin.ModelAdmin):
    list_display = ("data_element", "category_option_combo", "data_value_set", "session_id", "value", "created_at",
                    "updated_at")
    search_fields = ("data_element__name", "category_option_combo__name")
    list_filter = ("data_value_set",)


admin.site.register(DataValue, DataValueAdmin)


class DatasetDataElementAdmin(admin.ModelAdmin):
    list_display = ("data_element", "data_set",
                    "category_option_combo", "sort_order", "compulsory", "initialize_with_zero")
    search_fields = ("data_element__name",)
    list_filter = ("initialize_with_zero", "compulsory",
                   "data_set__name", "section__name")
    actions = ["toggle_initialize_with_zero", ]

    def toggle_initialize_with_zero(modeladmin, request, queryset):
        for dsde in queryset:
            dsde.initialize_with_zero = not dsde.initialize_with_zero
            dsde.save()
    toggle_initialize_with_zero.short_description = "Toggle Init With 0"


admin.site.register(DatasetDataElement, DatasetDataElementAdmin)
