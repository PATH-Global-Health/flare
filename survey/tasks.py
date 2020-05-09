from celery import shared_task
from .helpers import create_survey_result, mark_survey_result_complete

@shared_task
def create_survey_result_task(survey_pk, session_key, phone_number):
    create_survey_result(survey_pk, session_key, phone_number)

@shared_task
def mark_survey_result_complete_task(survey_pk, session_key, phone_number):
    mark_survey_result_complete(survey_pk, session_key, phone_number)