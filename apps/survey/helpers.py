# import os
# import yaml
# import json
# import logging
# from django.contrib.sessions.models import Session
# from .models import SurveyResult
# from django.conf import settings
#
# import requests
# from datetime import datetime, timedelta
# from django.conf import settings
# from django.db import connection
# from django.core import management
#
# logger = logging.getLogger(__name__)


# service_key = os.path.join(settings.BASE_DIR, 'ServiceAccountKey.json')
# cred = credentials.Certificate(service_key)
# firebase_admin.initialize_app(cred, {
#     'databaseURL': "https://flare-9f285.firebaseio.com"
# })

# def read_journey(journey):
#     journey.seek(0)
#     j = journey.read()
#     return yaml.full_load(j)
#
#
# def create_survey_result(survey_pk, session_key, phone_number):
#     try:
#         result = SurveyResult.objects.filter(session_id=session_key).first()
#         if result is None:
#             result = SurveyResult(survey_id=survey_pk, session_id=session_key, phone_number=phone_number)
#             result.save()
#     except Exception as ex:
#         logger.error(ex)
#
#
# def mark_survey_result_complete(survey_pk, session_key, phone_number):
#     try:
#         survey_result = SurveyResult.objects.filter(session_id=session_key, phone_number=phone_number).first()
#         if survey_result is None:
#             survey_result = SurveyResult(survey_id=survey_pk, session_id=session_key, phone_number=phone_number)
#
#         session = Session.objects.get(session_key=session_key)
#         data = session.get_decoded()
#
#         survey_result.result = data
#         survey_result.completed = True
#         survey_result.save()
#     except Exception as ex:
#         logger.error(ex)
#
#
# def copy_incomplete_data_2_survey_results():
#     results = SurveyResult.objects.filter(result=None)
#     for result in results:
#         try:
#             session = Session.objects.filter(session_key=result.session_id).first()
#             if session is not None:
#                 data = session.get_decoded()
#
#                 result.result = data
#                 result.completed = False
#                 result.save()
#         except Exception as ex:
#             logger.info(ex)
#
#
# def dict_fetch_all(cursor):
#     """Return all rows from a cursor as a dict"""
#     columns = [col[0] for col in cursor.description]
#     return [
#         dict(zip(columns, row))
#         for row in cursor.fetchall()
#     ]
#
#
# def check_missed_sessions_have_survey_data():
#     sql = """
#     SELECT session_key, completed
#     FROM django_session
#     LEFT JOIN survey_surveyresult
#     ON session_key=session_id
#     WHERE completed IS NULL;
#     """
#     session_keys = []
#     with connection.cursor() as cursor:
#         cursor.execute(sql)
#         session_keys = dict_fetch_all(cursor)
#
#     for key in session_keys:
#         try:
#             session = Session.objects.filter(session_key=key['session_key']).first()
#             if session is not None:
#                 data = session.get_decoded()
#                 r = yaml.load(str(data), Loader=yaml.FullLoader)
#                 if (('fever' in r and r['fever'] == '1') or
#                         ('cough' in r and r['cough'] == '1') or
#                         ('shortness_of_breath' in r and r['shortness_of_breath'] == '1')):
#                     if 'phone_number' in r:
#                         # TODO: Identify survey_id from the yaml data
#                         survey_result = SurveyResult(survey_id=1, session_id=key['session_key'],
#                                                      phone_number=r['phone_number'])
#                         survey_result.result = data
#                         survey_result.completed = False
#                         survey_result.save()
#         except Exception as ex:
#             logger.info(ex)
#
#
# """Cleanup expired sessions by using Django management command."""
#
#
# def clear_expired_session():
#     logger.info('CLEAR EXPIRED SESSION----------------------------------')
#     management.call_command("clearsessions", verbosity=0)
#
#
# """Get token to be included in every request to sync data."""


# def get_auth_header():
#     try:
#         response = requests.post(settings.CENTRAL_REPO_AUTH_URL, json={"UserName": settings.CENTRAL_REPO_USERNAME,
#                                                                        "Password": settings.CENTRAL_REPO_PASSWORD})
#         if response.status_code == 200:
#             return True, response.json()["token"]
#         else:
#             logger.error('AUTHENTICATION FAILED----------------------------------')
#             logger.error("Authentication failed with URL: {} username: {} and password: {}."
#                          .format(settings.CENTRAL_REPO_AUTH_URL,
#                                  settings.CENTRAL_REPO_USERNAME,
#                                  settings.CENTRAL_REPO_PASSWORD))
#             return False, None
#     except Exception as ex:
#         logger.error('AUTHENTICATION FAILED----------------------------------')
#         logger.error("Authentication failed with URL: {} username: {} and password: {}."
#                      .format(settings.CENTRAL_REPO_AUTH_URL,
#                              settings.CENTRAL_REPO_USERNAME,
#                              settings.CENTRAL_REPO_PASSWORD))
#         logger.error(ex)
#         return False, None
#
#
# def sync_survey_result_2_central_repo():
#     # Sync only those rows which are not posted, rejected and older than 10 minutes
#     time_threshold = datetime.now() - timedelta(minutes=10)
#     results = SurveyResult.objects.filter(created_at__lt=time_threshold, posted=None, rejected=None)
#     if results.count() > 0:
#         auth = get_auth_header()
#         headers = {'Authorization': 'Bearer {}'.format(auth[1])}
#         if auth[0]:
#             for res in results:
#                 if res.result is not None:
#                     r = yaml.load(res.result, Loader=yaml.FullLoader)
#                     if ((('fever' in r and r['fever'] == '1') or
#                          ('cough' in r and r['cough'] == '1') or
#                          ('shortness_of_breath' in r and r['shortness_of_breath'] == '1')) and
#                             ('region' in r and is_region_valid(r['region']))):
#
#                         data = prep_data(r)
#
#                         response = requests.post(settings.CENTRAL_REPO_CI_URL, json=json.loads(json.dumps(data)),
#                                                  headers=headers)
#
#                         if response.status_code == 200:
#                             res.posted = True
#                             res.save()
#                             logger.info(
#                                 'Data with phone number {} and session key {} is written to central repo.'.format(
#                                     res.phone_number, res.session_id))
#                         else:
#                             logger.error(
#                                 'Unable to send data. phone number {} and session key {}'.format(res.phone_number,
#                                                                                                  res.session_id))
#                             logger.error(json.loads(json.dumps(data)))
#                             logger.error(response.json())
#                     else:
#                         res.rejected = True
#                         res.save()


# REGIONS = {
#     "1": "Afar",
#     "2": "Amhara",
#     "3": "Beneshangul Gumuz",
#     "4": "Gambella",
#     "5": "Oromiya",
#     "6": "SNNP",
#     "7": "Somali",
#     "8": "Tigray",
#     "9": "Diredawa",
#     "10": "Addis Ababa",
#     "11": "Harari"
# }


# # def prep_data(r):
# #     data = {}
# #     assign_value(r, data, "fever", "fever", {'1': True, '2': False})
# #     assign_value(r, data, "cough", "cough", {'1': True, '2': False})
# #     assign_value(r, data, "shortness_of_breath", "breathingDifficulty", {'1': True, '2': False})
# #     assign_value(r, data, "sex", "sex", {'1': 'male', '2': 'female'}, "")
# #
# #     if 'name' in r:
# #         name = r["name"].split()
# #         if name.__len__() > 0:
# #             data["firstName"] = name[0]
# #         else:
# #             data["firstName"] = ""
# #
# #         if name.__len__() > 1:
# #             data["lastName"] = name[1]
# #         else:
# #             data["lastName"] = ""
# #     else:
# #         data["firstName"] = ""
# #         data["lastName"] = ""
# #
# #     if 'age' in r:
# #         data["age"] = r['age']
# #
# #     if 'phone_number' in r:
# #         data["PhoneNo"] = r['phone_number']
# #
# #     assign_value(r, data, "region", "Region", REGIONS)
# #     assign_value(r, data, "travel_history", "TravleHx", {'1': True, '2': False})
# #     assign_value(r, data, "has_contact", "HaveSex", {'1': True, '2': False})
# #
# #     data["version"] = 1
# #     data["source"] = "USSD"
# #     data["formStatus"] = "Incomplete"
# #
# #     current_date_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.003Z")
# #     data["createdDate"] = current_date_time
# #     data["modifiedDate"] = current_date_time
# #
# #     if "_ussd_airflow_last_updated" in r:
# #         data["callDate"] = format_date(r["_ussd_airflow_last_updated"])
# #     else:
# #         data["callDate"] = current_date_time
#
#     return data


# def is_region_valid(region):
#     if region in REGIONS.keys():
#         return True
#
#     return False


def assign_value(r, data, ussd_key, repo_key, values, default=None):
    if ussd_key in r:
        if r[ussd_key] in values.keys():
            data[repo_key] = values[r[ussd_key]]
        elif default is not None:
            data[repo_key] = default


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
