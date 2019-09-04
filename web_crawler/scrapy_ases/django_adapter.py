
# ===================|| SETUP DJANGO ORM ||=================== #

import sys
import os
import django

project_root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django_path = os.path.join(project_root_path, 'web_app')
sys.path.append(django_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_app.settings')
django.setup()

from django.utils.timezone import make_aware

from certifications.models import Page, EvaluationReport

# =================|| FUNCTIONS FOR SPIDER ||================= #

reports_path = os.path.join(project_root_path, 'reports')

if not 'reports' in os.listdir(project_root_path):
    os.mkdir(reports_path)

def active_pages():
    active_pages = []
    for page in Page.objects.all():
        if page.certification.is_active:
            active_pages.append(page)
    return active_pages

def update_page_url(page, url):
    ''' (Page, string)
    '''
    page.url = url
    page.save()

def save_report_to_database(page, grade, creation_date_time):
    ''' (Page, int, datetime, bool)
    '''
    report = EvaluationReport(
        page = page, 
        grade = grade, 
        creation_date_time = make_aware(creation_date_time),
    )
    report.save()
