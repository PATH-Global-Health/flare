from celery import shared_task
from .helpers import create_survey_result, \
                      mark_survey_result_complete, \
                      sync_survey_result_2_firebase, \
                      copy_incomplete_data_2_survey_results, \
                      sync_survey_result_2_central_repo

@shared_task
def create_survey_result_task(survey_pk, session_key, phone_number):
    create_survey_result(survey_pk, session_key, phone_number)

@shared_task
def mark_survey_result_complete_task(survey_pk, session_key, phone_number):
    mark_survey_result_complete(survey_pk, session_key, phone_number)

@shared_task
def sync_survey_result_2_firebase_task():
    sync_survey_result_2_firebase()

@shared_task
def copy_incomplete_data_2_survey_results_task():
    copy_incomplete_data_2_survey_results()
    
@shared_task
def sync_survey_result_2_central_repo_task():
    sync_survey_result_2_central_repo()
    