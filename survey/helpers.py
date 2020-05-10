import yaml
import logging
from django.contrib.sessions.models import Session
from .models import SurveyResult

logger = logging.getLogger(__name__)

def read_journey(journey):
    journey.seek(0)
    j = journey.read()
    return yaml.full_load(j)

def create_survey_result(survey_pk, session_key, phone_number):
    try:
        result = SurveyResult.objects.filter(session_id = session_key).first()
        if result == None:
            result = SurveyResult(survey_id=survey_pk, session_id=session_key, phone_number=phone_number)
            result.save()
    except Exception as ex:
        logger.error(ex)

def mark_survey_result_complete(survey_pk, session_key, phone_number):
    try:
        survey_result = SurveyResult.objects.filter(session_id = session_key, phone_number = phone_number).first()
        if survey_result == None:
            survey_result = SurveyResult(survey_id=survey_pk, session_id=session_key, phone_number=phone_number)

        session = Session.objects.get(session_key=session_key)
        data = session.get_decoded()

        survey_result.result = data
        survey_result.completed = True
        survey_result.save()
    except Exception as ex:
        logger.error(ex)


# def validate_ussd_journey(journey):

#     if 'initialize_survey' not in journey:
#         return (False, 'initialize_survey is missing')

#     if 'type' not in journey['initialize_survey']:
#         return (False, {'initialize_survey': 'type is missing in initialize_survey screen'})
    
#     if journey['initialize_survey']['type'] != 'update_session_screen':
#         return (False, {'initialize_survey': 'initialize_survey screen type should be update_session_screen'})

#     if 'values_to_update' not in journey['initialize_survey']:
#         return (False, {'initialize_survey', 'values_to_update is missing in initialize_survey screen'})

#     errors = []
#     is_valid = True
#     values_to_update = ['endpoint', 'survey_id']
#     for val in values_to_update:
#         found = False
#         for s in journey['initialize_survey']['values_to_update']:
#             if 'key' in s and s['key'] == val:
#                 found = True
#                 break
#         if not found:
#             is_valid = False
#             errors.append('{} is missing from values_to_update in initialize_survey screen'.format(val))

#     return (is_valid, errors)

# def get_survey_endpoint_and_id(journey):
#     result = {}
#     values_to_update = ['endpoint', 'survey_id']
#     for val in values_to_update:
#         for s in journey['initialize_survey']['values_to_update']:
#             if 'key' in s and s['key'] == val:
#                 result[val]=s['value']
#                 break

#     return result