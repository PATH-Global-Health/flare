import json
import yaml
import logging
from message.models import Message
from subscriber.models import Subscriber
from survey.models import Survey, SurveyResult
from collections import OrderedDict

logger = logging.getLogger(__name__)

def get_total_messages():
    messages_count = 0
    try:
        messages_count = Message.objects.count()
        logger.info("{} total messages".format(messages_count))
    except Exception as ex:
        logger.error(ex)

    return messages_count

def get_total_subscribers():
    subscribers_count = 0
    try:
        subscribers_count = Subscriber.objects.count()
        logger.info("{} total subscribers".format(subscribers_count))
    except Exception as ex:
        logger.error(ex)

    return subscribers_count

def get_total_surveys():
    surveys_count = 0
    try:
        surveys_count = Survey.objects.count()
        logger.info("{} total surveys".format(surveys_count))
    except Exception as ex:
        logger.error(ex)

    return surveys_count

def get_total_survey_result():
    survey_result_count = 0
    try:
        results = SurveyResult.objects.all()

        for res in results:
            if res.result != None:
                r = yaml.load(res.result, Loader=yaml.FullLoader)
                if ('fever' in r and r['fever']=='1') or ('cough' in r and r['cough']=='1') or ('shortness_of_breath' in r and r['shortness_of_breath']=='1'):
                    survey_result_count += 1
        logger.info("{} total survey result".format(survey_result_count))
    except Exception as ex:
        logger.error(ex)

    return survey_result_count

def get_suspects_report():
    
    result_by_region = {
        'labels': ["Afar", "Amhara", "Beneshangul Gumuz", "Gambella", "Oromiya", "SNNP", "Somali", "Tigray", "Diredawa", "Addis Ababa", "Harari"],
        'datasets': []
    }
    
    result_by_age = {
        'labels': ["< 5", "5 - 14", "15 - 24", "25 - 34", "35 - 44", "45 - 59", "60 >"],
        'datasets': []
    }

    result_by_sex = {
        'labels': ["Male", "Female"],
        'datasets': []
    }
    
    data_by_region = {'1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0, '10':0, '11':0}
    data_by_sex = {'1':0, '2':0}
    data_by_age = {"< 5":0, "5 - 14":0, "15 - 24":0, "25 - 34":0, "35 - 44":0, "45 - 59":0, "60 >":0}

    results = SurveyResult.objects.all()

    for res in results:
        if res.result != None:
            r = yaml.load(res.result, Loader=yaml.FullLoader)
            if ('fever' in r and r['fever']=='1') or ('cough' in r and r['cough']=='1') or ('shortness_of_breath' in r and r['shortness_of_breath']=='1'):
                data_by_region[r['region']] += 1
                data_by_sex[r['sex']] += 1
                data_by_age[age_category(int(r['age']))] += 1

    result_by_region['datasets'].append({'data': list(data_by_region.values())})

    male = int(round((int(data_by_sex['1'])/ (int(data_by_sex['1']) + int(data_by_sex['2'])))*100, 0))
    female = int(round((int(data_by_sex['2'])/ (int(data_by_sex['1']) + int(data_by_sex['2'])))*100, 0))
    result_by_sex['datasets'].append({'data': [male, female]})
    
    result_by_age['datasets'].append({'data': list(data_by_age.values())})

    logger.info('Suspects by region {}'.format(json.dumps(result_by_region)))
    logger.info('Suspects by sex {}'.format(json.dumps(result_by_sex)))
    logger.info('Suspects by age {}'.format(json.dumps(result_by_age)))

    return (json.dumps(result_by_region), json.dumps(result_by_sex), json.dumps(result_by_age))

def age_category(age):
    if age < 5:
        return '< 5'
    if age >=5 and age <= 14:
        return '5 - 14'
    if age >=15 and age <= 24:
        return '15 - 24'
    if age >=25 and age <= 34:
        return '25 - 34'
    if age >=35 and age <= 44:
        return '35 - 44'
    if age >=45 and age <= 59:
        return '45 - 59'
    
    return '60 >'