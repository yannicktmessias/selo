from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime, date, timedelta
from pytz import timezone
import os
import shutil

from .forms import (
    CertificationApplicantForm,
    CertificationCreationForm,
    CertificationChangeForm,
    PageCreationForm,
)
from .models import Certification, Page, EvaluationReport
from applicants.models import Applicant, LegalRepresentative

from accounts.decorators import read_write_permission_required, admin_required

project_root_path = os.path.dirname(settings.BASE_DIR)
reports_path = os.path.join(project_root_path, 'reports')

def get_past_days(number_of_days):
    dates = []
    today = datetime.now(timezone(settings.TIME_ZONE)).date()
    for i in range(number_of_days):
        date = today - timedelta(days = i)
        dates.append(date)

    return dates

def get_past_reports(pages, dates):
    reports = {}
    for page in pages:
        page_reports = EvaluationReport.objects.filter(page=page)
        reports[page] = []
        for date in dates:
            date_page_report = page_reports.filter(
                creation_date_time__year=date.year,
                creation_date_time__month=date.month,
                creation_date_time__day=date.day,
            )
            if date_page_report:
                date_page_report = date_page_report[0]
            else:
                date_page_report = EvaluationReport(
                    page=page, 
                    grade=0,
                    creation_date_time=date,
                    page_found=False,
                )
            reports[page].append(date_page_report)

    return reports

def get_above_links_count(pages, reports, dates, last_evaluation):
    if last_evaluation == '':
        return len(pages)
    above_links_count = 0
    for i, date in enumerate(dates):
        if date.day == last_evaluation.day:
            break
    for page in pages:
        if reports[page][i].succeed():
            above_links_count += 1
    return above_links_count

@login_required(login_url='login')
def certification_info(request, sei_number, number_of_days = 4):
    certification = Certification.objects.get(sei_number=sei_number)
    applicant = certification.applicant
    legal_representative = LegalRepresentative.objects.filter(applicant_represented=applicant)
    pages = Page.objects.filter(certification=certification)
    if legal_representative:
        legal_representative = legal_representative[0]
    dates = get_past_days(number_of_days)
    reports = get_past_reports(pages, dates)
    certification_reports = EvaluationReport.objects.filter(page__certification=certification)
    if len(certification_reports) > 0:
        last_evaluation = certification_reports.latest('creation_date_time').creation_date_time
    else:
        last_evaluation = ''
    above_links_count = get_above_links_count(pages, reports, dates, last_evaluation)
    below_links_count = len(pages) - above_links_count
    args = {
        'certification': certification,
        'applicant': applicant,
        'legal_representative': legal_representative,
        'pages': pages,
        'dates': dates,
        'reports': reports,

        'last_evaluation': last_evaluation,
        'above_links_count': above_links_count,
        'below_links_count': below_links_count,
    }
    return render(request, 'certifications/certification_info.html', args)

@login_required(login_url='login')
def report_show(request, sei_number, page_id, date_time):
    certification = Certification.objects.get(sei_number=sei_number)
    applicant = certification.applicant
    page = Page.objects.get(id=page_id)
    cleaned_url = page.url.replace('/', ",-'")

    applicant_path = os.path.join(reports_path, applicant.cpf_cnpj)
    certification_path = os.path.join(applicant_path, certification.sei_number)
    url_path = os.path.join(certification_path, cleaned_url)
    pdf_path = os.path.join(url_path, date_time + '.pdf')

    with open(pdf_path, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'filename='+date_time.replace(':', '-')
        return response

def create_link_forms_from_database(certification):
    links = Page.objects.filter(certification=certification)
    link_forms = []
    for link in links:
        link_form = PageCreationForm(instance=link)
        link_forms.append(link_form)

    return link_forms


def create_link_forms_from_post_request(post = {}):
    link_forms = []
    for i in range(1, 21):
        if post.get('link_'+str(i), '') != '':
            args = {
                'url': post.get('link_'+str(i), ''),
            }
            link_form = PageCreationForm(args)
            link_forms.append(link_form)

    return link_forms

def update_certification_links(certification, link_forms):
    for link_form in link_forms:
        if link_form.is_valid():
            page = link_form.save(commit=False)
            page.certification = certification
            page.save()

    pages = Page.objects.filter(certification=certification)
    for page in pages:
        page_is_not_in_link_forms = True
        for link_form in link_forms:
            if link_form.data['url'].strip() == page.url:
                page_is_not_in_link_forms = False
                break
        if page_is_not_in_link_forms:
            applicant = certification.applicant
            cleaned_url = page.url.replace('/', ",-'")

            applicant_path = os.path.join(reports_path, applicant.cpf_cnpj)
            certification_path = os.path.join(applicant_path, certification.sei_number)
            url_path = os.path.join(certification_path, cleaned_url)

            if cleaned_url in os.listdir(certification_path):
                shutil.rmtree(url_path)

            page.delete()

@login_required(login_url='login')
@read_write_permission_required(login_url='login')
def edit_certification(request, sei_number):
    certification = Certification.objects.get(sei_number=sei_number)
    applicant = certification.applicant

    if request.method == 'POST':
        form = CertificationChangeForm(request.POST, instance=certification)
        link_forms = create_link_forms_from_post_request(request.POST)

        if form.is_valid():
            certification = form.save(commit=False)
            if certification.domain[-1] != '/':
                certification.domain += '/'
            certification.save()
            certification = Certification.objects.get(sei_number=sei_number)
            update_certification_links(certification, link_forms)
            return redirect('certification_info', sei_number=sei_number)
        
        args = {
            'form': form, 
            'certification': certification, 
            'applicant': applicant,
            'link_forms': link_forms,
        }
        return render(request, 'certifications/edit_certification.html', args)
    else:
        form = CertificationChangeForm(instance=certification)
        link_forms = create_link_forms_from_database(certification)

        args = {
            'form': form, 
            'certification': certification, 
            'applicant': applicant, 
            'link_forms': link_forms,
        }
        return render(request, 'certifications/edit_certification.html', args)

@login_required(login_url='login')
@read_write_permission_required(login_url='login')
@admin_required(login_url='login')
def delete_certification(request, sei_number):
    return redirect('delete_certification_confirmation', sei_number=sei_number)

@login_required(login_url='login')
@read_write_permission_required(login_url='login')
@admin_required(login_url='login')
def delete_certification_confirmation(request, sei_number):
    certification = Certification.objects.get(sei_number=sei_number)
    applicant = certification.applicant

    if request.method == 'POST':
        applicant_path = os.path.join(reports_path, applicant.cpf_cnpj)
        certification_path = os.path.join(applicant_path, certification.sei_number)

        if certification.sei_number in os.listdir(applicant_path):
            shutil.rmtree(certification_path)

        certification.delete()
        return redirect('list_certifications')
    else:
        args = {'certification': certification, 'applicant': applicant}
        return render(request, 'certifications/delete_certification_confirmation.html', args)

@login_required(login_url='login')
@read_write_permission_required(login_url='login')
def activate_certification(request, sei_number):
    certification = Certification.objects.get(sei_number=sei_number)
    certification.is_active = True
    certification.save()
    return redirect('certification_info', sei_number=certification.sei_number)

@login_required(login_url='login')
@read_write_permission_required(login_url='login')
def inactivate_certification(request, sei_number):
    return redirect('inactivate_certification_confirmation', sei_number=sei_number)

def inactivate_certification_confirmation(request, sei_number):
    certification = Certification.objects.get(sei_number=sei_number)
    applicant = certification.applicant

    if request.method == 'POST':
        certification.is_active = False
        certification.save()
        return redirect('certification_info', sei_number=certification.sei_number)
    else:
        args = {'certification': certification, 'applicant': applicant}
        return render(request, 'certifications/inactivate_certification_confirmation.html', args)

@login_required(login_url='login')
@read_write_permission_required(login_url='login')
def new_certification_applicant(request):
    not_found = False

    if request.method == 'POST':
        form = CertificationApplicantForm(request.POST)
        if form.is_valid():
            if Applicant.objects.filter(cpf_cnpj=request.POST['cpf_cnpj']):
                return redirect('new_certification', cpf_cnpj=request.POST['cpf_cnpj'])
            else:
                not_found = True

        args = {'form': form, 'not_found': not_found}
        return render(request, 'certifications/new_certification_applicant.html', args)
    else:
        form = CertificationApplicantForm()

        args = {'form': form, 'not_found': not_found}
        return render(request, 'certifications/new_certification_applicant.html', args)

@login_required(login_url='login')
@read_write_permission_required(login_url='login')
def new_certification(request, cpf_cnpj):
    applicant = Applicant.objects.get(cpf_cnpj=cpf_cnpj)

    if request.method == 'POST':
        form = CertificationCreationForm(request.POST)
        link_forms = create_link_forms_from_post_request(request.POST)
        if form.is_valid():
            certification = form.save(commit=False)
            certification.applicant = applicant
            if certification.domain[-1] != '/':
                certification.domain += '/'
            certification.save()
            certification = Certification.objects.get(sei_number=request.POST['sei_number'])
            update_certification_links(certification, link_forms)
            return redirect('certification_info', sei_number=certification.sei_number)

        args = {'form': form, 'applicant': applicant, 'link_forms': link_forms}
        return render(request, 'certifications/new_certification.html', args)
    else:
        form = CertificationCreationForm()
        link_forms = create_link_forms_from_post_request()

        args = {'form': form, 'applicant': applicant, 'link_forms': link_forms}
        return render(request, 'certifications/new_certification.html', args)

@login_required(login_url='login')
def list_certifications(request):
    certifications = Certification.objects.filter(is_active=True)
    last_evaluation = {}
    above_links_count = {}
    below_links_count = {}

    for certification in certifications:
        pages = Page.objects.filter(certification=certification)
        dates = get_past_days(7)
        reports = get_past_reports(pages, dates)
        certification_reports = EvaluationReport.objects.filter(page__certification=certification)
        if len(certification_reports) > 0:
            last_evaluation[certification] = certification_reports.latest('creation_date_time').creation_date_time
        else:
            last_evaluation[certification] = ''
        above_links_count[certification] = get_above_links_count(pages, reports, dates, last_evaluation[certification])
        below_links_count[certification] = len(pages) - above_links_count[certification]

    args = {
        'certifications': certifications,
        'last_evaluation': last_evaluation,
        'above_links_count': above_links_count,
        'below_links_count': below_links_count,
    }
    return render(request, 'certifications/list_certifications.html', args)

@login_required(login_url='login')
def search_certification(request):
    search_term = request.GET.get('search_for', '')
    where = request.GET.get('in', '')
    if where == 'domain':
        certifications = Certification.objects.filter(domain__icontains=search_term)
        where = 'Domínio'
    elif where == 'sei_number':
        certifications = Certification.objects.filter(sei_number__icontains=search_term)
        where = 'Processo SEI'
    elif where == 'applicant':
        certifications = Certification.objects.filter(applicant__name__icontains=search_term)
        where = 'Requerente'
    else:
        certifications = Certification.objects.all()
        where = 'indefinido'

    last_evaluation = {}
    above_links_count = {}
    below_links_count = {}

    for certification in certifications:
        pages = Page.objects.filter(certification=certification)
        dates = get_past_days(7)
        reports = get_past_reports(pages, dates)
        certification_reports = EvaluationReport.objects.filter(page__certification=certification)
        if len(certification_reports) > 0:
            last_evaluation[certification] = certification_reports.latest('creation_date_time').creation_date_time
        else:
            last_evaluation[certification] = ''
        above_links_count[certification] = get_above_links_count(pages, reports, dates, last_evaluation[certification])
        below_links_count[certification] = len(pages) - above_links_count[certification]

    args = {
        'search_term': search_term, 
        'where': where, 
        'certifications': certifications,
        'last_evaluation': last_evaluation,
        'above_links_count': above_links_count,
        'below_links_count': below_links_count,
    }
    return render(request, 'certifications/search_certification.html', args)

@login_required(login_url='login')
def index(request):
    return redirect('list_certifications')
