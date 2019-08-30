from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import (
    CertificationApplicantForm,
    CertificationCreationForm,
    CertificationChangeForm,
    PageCreationForm,
)
from .models import Certification, Page
from applicants.models import Applicant, LegalRepresentative

@login_required(login_url='login')
def certification_info(request, sei_number):
    certification = Certification.objects.get(sei_number=sei_number)
    applicant = certification.applicant
    legal_representative = LegalRepresentative.objects.filter(applicant_represented=applicant)
    pages = Page.objects.filter(certification=certification)
    if legal_representative:
        legal_representative = legal_representative[0]
    args = {
        'certification': certification,
        'applicant': applicant,
        'legal_representative': legal_representative,
        'pages': pages
    }
    return render(request, 'certifications/certification_info.html', args)

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
            if link_form.data['url'] == page.url:
                page_is_not_in_link_forms = False
        if page_is_not_in_link_forms:
            page.delete()

@login_required(login_url='login')
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
def delete_certification(request, sei_number):
    return redirect('delete_certification_confirmation', sei_number=sei_number)

@login_required(login_url='login')
def delete_certification_confirmation(request, sei_number):
    certification = Certification.objects.get(sei_number=sei_number)
    applicant = certification.applicant

    if request.method == 'POST':
        certification.delete()
        return redirect('list_certifications')
    else:
        args = {'certification': certification, 'applicant': applicant}
        return render(request, 'certifications/delete_certification_confirmation.html', args)

@login_required(login_url='login')
def activate_certification(request, sei_number):
    certification = Certification.objects.get(sei_number=sei_number)
    certification.is_active = True
    certification.save()
    return redirect('certification_info', sei_number=certification.sei_number)

@login_required(login_url='login')
def inactivate_certification(request, sei_number):
    certification = Certification.objects.get(sei_number=sei_number)
    certification.is_active = False
    certification.save()
    return redirect('certification_info', sei_number=certification.sei_number)

@login_required(login_url='login')
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
    certifications = Certification.objects.all()
    return render(request, 'certifications/list_certifications.html', {'certifications': certifications})

@login_required(login_url='login')
def search_certification(request):
    search_term = request.GET.get('search_for', '')
    where = request.GET.get('in', '')
    if where == 'domain':
        certifications = Certification.objects.filter(domain__icontains=search_term)
        where = 'Domínio'
    elif where == 'applicant':
        certifications = Certification.objects.filter(applicant__name__icontains=search_term)
        where = 'Requerente'
    else:
        certifications = Certification.objects.all()
        where = 'indefinido'
    args = {'search_term': search_term, 'where': where, 'certifications': certifications}
    return render(request, 'certifications/search_certification.html', args)

@login_required(login_url='login')
def index(request):
    cert_1 = {
        'id': 1,
        'domain': 'prefeitura.sp.gov.br/',
        'applicant': 'Prefeitura do Cidade de São Paulo',
        'grant_date': '12/02/2019',
        'below_links_count': 0,
        'above_links_count': 13,
        'last_evaluation': '19:42 21/04/2019',
        'link': '',
    }
    cert_2 = {
        'id': 2,
        'domain': 'camarasuzano.sp.gov.br/',
        'applicant': 'Câmara Municipal de Suzano',
        'grant_date': '12/02/2019',
        'below_links_count': 1,
        'above_links_count': 19,
        'last_evaluation': '19:42 21/04/2019',
        'link': '',
    }
    cert_3 = {
        'id': 3,
        'domain': 'samsung.com.br/',
        'applicant': 'Samsung',
        'grant_date': '12/02/2019',
        'below_links_count': 0,
        'above_links_count': 2,
        'last_evaluation': '19:42 21/04/2019',
        'link': '',
    }

    args = {
        'certifications': [cert_1, cert_2, cert_3]
    }

    return render(request, 'home.html', args)
