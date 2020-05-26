import os
import yaml
import json
import logging
from django.contrib.sessions.models import Session
from .models import SurveyResult
from django.conf import settings
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db
import requests
from datetime import datetime
from django.conf import settings
from django.db import connection
from django.core import management

logger = logging.getLogger(__name__)

# service_key = os.path.join(settings.BASE_DIR, 'ServiceAccountKey.json')
# cred = credentials.Certificate(service_key)
# firebase_admin.initialize_app(cred, {
#     'databaseURL': "https://flare-9f285.firebaseio.com"
# })

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

# def sync_survey_result_2_firebase():
#     ref = db.reference('covid19')
#     result_ref = ref.child('survey_result')

#     results = SurveyResult.objects.filter(posted=None, rejected=None)
#     for res in results:
#         if res.result != None:
#             r = yaml.load(res.result, Loader=yaml.FullLoader)
#             if ('fever' in r and r['fever']=='1') or ('cough' in r and r['cough']=='1') or ('shortness_of_breath' in r and r['shortness_of_breath']=='1'):
#                 result_ref.child("{}".format(res.id)).set({
#                     'phone_number': res.phone_number,
#                     'session_key': res.session_id,
#                     'fever': r['fever'],
#                     'cough': r['cough'],
#                     'shortness_of_breath': r['shortness_of_breath'],
#                     'name': r['name'],
#                     'age': r['age'],
#                     'sex': r['sex'],
#                     'region': r['region'],
#                     'travel_history': r['travel_history'],
#                     'has_contact': r['has_contact'],
#                     'last_updated': r['_ussd_airflow_last_updated']
#                 })
#                 res.posted = True
#                 res.save()
#                 logger.info('Data with phone number {} and session key {} is written to firebase.'.format(res.phone_number, res.session_id))
#             else:
#                 res.rejected = True
#                 res.save()

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
            logger.info(ex)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
                
def check_missed_sessions_have_survey_data():
    sql = """
    SELECT session_key, completed 
    FROM django_session 
    LEFT JOIN survey_surveyresult 
    ON session_key=session_id 
    WHERE completed IS NULL;
    """
    session_keys = []
    with connection.cursor() as cursor:
        cursor.execute(sql)
        session_keys = dictfetchall(cursor)

    for key in session_keys:
        try:
            session = Session.objects.filter(session_key=key['session_key']).first()
            if session != None:
                data = session.get_decoded()
                r = yaml.load(str(data), Loader=yaml.FullLoader)
                if ('fever' in r and r['fever']=='1') or ('cough' in r and r['cough']=='1') or ('shortness_of_breath' in r and r['shortness_of_breath']=='1'):
                    if 'phone_number' in r:
                        # TODO: Identify survey_id from the yaml data
                        survey_result = SurveyResult(survey_id=1, session_id=key['session_key'], phone_number=r['phone_number'])
                        survey_result.result = data
                        survey_result.completed = False
                        survey_result.save()
        except Exception as ex:
            logger.info(ex)

"""Cleanup expired sessions by using Django management command."""
def clear_expired_session():
    logger.info('CLEAR EXPIRED SESSION----------------------------------')
    management.call_command("clearsessions", verbosity=0)
    
"""Get token to be included in every request to sync data."""    
def get_auth_header():

    try:
        response = requests.post(settings.CENTRAL_REPO_AUTH_URL, json={"UserName":settings.CENTRAL_REPO_USERNAME, "Password":settings.CENTRAL_REPO_PASSWORD})
        if response.status_code == 200:
            return (True, response.json()["token"])
        else:
            logger.error('AUTHENTICATION FAILED----------------------------------')
            logger.error("Authenticatoin failed with URL: {} username: {} and password: {}."
                         .format(settings.CENTRAL_REPO_AUTH_URL,
                                 settings.CENTRAL_REPO_USERNAME,
                                 settings.CENTRAL_REPO_PASSWORD))
            return (False, None)
    except Exception as ex:
        logger.error('AUTHENTICATION FAILED----------------------------------')
        logger.error("Authenticatoin failed with URL: {} username: {} and password: {}."
                         .format(settings.CENTRAL_REPO_AUTH_URL,
                                 settings.CENTRAL_REPO_USERNAME,
                                 settings.CENTRAL_REPO_PASSWORD))
        logger.error(ex)
        return (False, None)
    
def sync_survey_result_2_central_repo():
    
    results = SurveyResult.objects.filter(posted=None, rejected=None)
    if results.count()>0:
        auth = get_auth_header()
        headers={'Authorization': 'Bearer {}'.format(auth[1])}
        if auth[0]:
            for res in results:
                if res.result != None:
                    r = yaml.load(res.result, Loader=yaml.FullLoader)
                    if ('fever' in r and r['fever']=='1') or 
                    ('cough' in r and r['cough']=='1') or 
                    ('shortness_of_breath' in r and r['shortness_of_breath']=='1') or
                    ('region' in r):

                        data = prep_data(r)

                        response = requests.post(settings.CENTRAL_REPO_CI_URL, json=json.loads(json.dumps(data)), headers=headers)
                        
                        if response.status_code==200:
                            res.posted = True
                            res.save()
                            logger.info('Data with phone number {} and session key {} is written to central repo.'.format(res.phone_number, res.session_id))
                        else:
                            logger.error('Unable to send data. phone number {} and session key {}'.format(res.phone_number, res.session_id))
                            logger.error(response.json())
                    else:
                        res.rejected = True
                        res.save()

def prep_data(r):
    data = {}
    assign_value(r, data, "fever", "fever", {'1':True, '2': False})
    assign_value(r, data, "cough", "cough", {'1':True, '2': False})
    assign_value(r, data, "shortness_of_breath", "breathingDifficulty", {'1':True, '2': False})
    assign_value(r, data, "sex", "sex", {'1':'male', '2': 'female'})
    
    if 'name' in r:
        name = r["name"].split()
        if name.__len__() > 0:
            data["firstName"] = name[0]
        else:
            data["firstName"] = ""
            
        if name.__len__() > 1:
            data["lastName"] = name[1]
        else:
            data["lastName"] = ""
    else:
        data["firstName"] = ""
        data["lastName"] = ""
    
    if 'age' in r:
        data["age"] = r['age']
    else:
        data["age"] = ""
    
    if 'phone_number' in r:
        data["PhoneNo"] = r['phone_number']
    
    assign_value(r, data, "region", "Region", {
        "1": "Afar",
        "2": "Amhara",
        "3": "Beneshangul Gumuz",
        "4": "Gambella",
        "5": "Oromiya",
        "6": "SNNP",
        "7": "Somali",
        "8": "Tigray",
        "9": "Diredawa",
        "10": "Addis Ababa",
        "11": "Harari"
    })
    assign_value(r, data, "travel_history", "TravleHx", {'1':True, '2': False})
    assign_value(r, data, "has_contact", "HaveSex", {'1':True, '2': False})

    data["version"]=1
    data["source"]="USSD"
    data["formStatus"] = "Incomplete"
    
    current_date_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.003Z")
    data["createdDate"] = current_date_time
    data["modifiedDate"] = current_date_time
    
    if "_ussd_airflow_last_updated" in r:
        data["callDate"] = format_date(r["_ussd_airflow_last_updated"])
    else:
        data["callDate"] = current_date_time
    
    return data
    
def assign_value(r, data, ussd_key, repo_key, values):
    if ussd_key in r:
        if r[ussd_key] in values.keys():
            data[repo_key] = values[r[ussd_key]]
        else:
            data[repo_key] = ""
            
def format_date(d):
    da = d.split(" ")
    formatted_date = ""
    if da.__len__() > 0:
        formatted_date = da[0]
    if da.__len__() > 1:
        da = da[1].split(".")
        if da.__len__() > 0:
            formatted_date = "{}T{}.003Z".format(formatted_date, da[0])
    return formatted_date
        
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