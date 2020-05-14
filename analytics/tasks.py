from celery import shared_task
from .helpers import get_total_messages, get_total_subscribers, get_total_surveys, get_total_survey_result, get_suspects_report
from .models import Report

@shared_task
def generate_report():
    report = Report()
    report.total_messages = get_total_messages()
    report.total_subscribers = get_total_subscribers()
    report.total_surveys = get_total_surveys()
    report.total_suspects = get_total_survey_result()
    
    rep = get_suspects_report()

    report.suspects_by_region = rep[0]
    report.suspects_by_sex = rep[1]
    report.suspects_by_age = rep[2]

    report.save()


    