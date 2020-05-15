import os
import yaml
import logging
from django.contrib.sessions.models import Session
from .models import SurveyResult
from django.conf import settings
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

logger = logging.getLogger(__name__)

service_key = os.path.join(settings.BASE_DIR, 'ServiceAccountKey.json')
cred = credentials.Certificate(service_key)
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://flare-9f285.firebaseio.com"
})

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

def sync_survey_result_2_firebase():
    ref = db.reference('covid19')
    result_ref = ref.child('survey_result')

    results = SurveyResult.objects.filter(posted=None, rejected=None)
    for res in results:
        if res.result != None:
            r = yaml.load(res.result, Loader=yaml.FullLoader)
            if ('fever' in r and r['fever']=='1') or ('cough' in r and r['cough']=='1') or ('shortness_of_breath' in r and r['shortness_of_breath']=='1'):
                result_ref.child("{}".format(res.id)).set({
                    'phone_number': res.phone_number,
                    'session_key': res.session_id,
                    'fever': r['fever'],
                    'cough': r['cough'],
                    'shortness_of_breath': r['shortness_of_breath'],
                    'name': r['name'],
                    'age': r['age'],
                    'sex': r['sex'],
                    'region': r['region'],
                    'travel_history': r['travel_history'],
                    'has_contact': r['has_contact'],
                    'last_updated': r['_ussd_airflow_last_updated']
                })
                res.posted = True
                res.save()
                logger.info('Data with phone number {} and session key {} is written to firebase.'.format(res.phone_number, res.session_id))
            else:
                res.rejected = True
                res.save()

def copy_incomplete_data_2_survey_results():
    results = SurveyResult.objects.filter(result=None)
    for result in results:
        try:
            session = Session.objects.filter(session_key=result.session_id).first()
            if session != None:
                data = session.get_decoded()

                result.result = data
                result.completed = False
                result.save()
        except Exception as ex:
            logger.log(ex)
    
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