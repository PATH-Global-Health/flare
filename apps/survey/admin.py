from django.contrib import admin
from apps.survey.models import Survey, SurveyResult

admin.site.register(Survey)
admin.site.register(SurveyResult)
