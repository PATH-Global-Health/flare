from django.contrib import admin
from apps.survey.models import Survey, SurveyResult


class SurveyAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "published")
    list_filter = ("title", "published")
    search_fields = ("title", "slug")


admin.site.register(Survey, SurveyAdmin)
admin.site.register(SurveyResult)
