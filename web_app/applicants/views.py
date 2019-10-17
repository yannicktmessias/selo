from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os
import shutil

from .forms import (
    ApplicantCreationForm,
    ApplicantChangeForm,
    LegalRepresentativeCreationForm,
    LegalRepresentativeChangeForm,
)
from .models import Applicant, LegalRepresentative

from accounts.decorators import read_write_permission_required, admin_required

project_root_path = os.path.dirname(settings.BASE_DIR)
reports_path = os.path.join(project_root_path, 'reports')

@login_required(login_url='login')
def applicant_info(request, cpf_cnpj):
    applicant = Applicant.objects.get(cpf_cnpj=cpf_cnpj)
    legal_representative = LegalRepresentative.objects.filter(applicant_represented=applicant)
    if legal_representative:
        legal_representative = legal_representative[0]
    args = {'applicant': applicant, 'legal_representative': legal_representative}
    return render(request, 'applicants/applicant_info.html', args)

@login_required(login_url='login')
@read_write_permission_required(login_url='login')
def edit_applicant(request, cpf_cnpj):
    applicant = Applicant.objects.get(cpf_cnpj=cpf_cnpj)

    if request.method == 'POST':
        form = ApplicantChangeForm(request.POST, instance=applicant)

        if form.is_valid():
            form.save()
            return redirect('applicant_info', cpf_cnpj=cpf_cnpj)
        
        args = {'form': form, 'applicant': applicant}
        return render(request, 'applicants/edit_applicant.html', args)
    else:
        form = ApplicantChangeForm(instance=applicant)

        args = {'form': form, 'applicant': applicant}
        return render(request, 'applicants/edit_applicant.html', args)

@login_required(login_url='login')
@read_write_permission_required(login_url='login')
def edit_legal_representative(request, cpf_cnpj):
    applicant = Applicant.objects.get(cpf_cnpj=cpf_cnpj)
    legal_representative = LegalRepresentative.objects.get(applicant_represented=applicant)

    if request.method == 'POST':
        form = LegalRepresentativeChangeForm(request.POST, instance=legal_representative)

        if form.is_valid():
            form.save()
            return redirect('applicant_info', cpf_cnpj=cpf_cnpj)
        
        args = {'form': form, 'applicant': applicant, 'legal_representative': legal_representative}
        return render(request, 'applicants/edit_legal_representative.html', args)
    else:
        form = LegalRepresentativeChangeForm(instance=legal_representative)

        args = {'form': form, 'applicant': applicant, 'legal_representative': legal_representative}
        return render(request, 'applicants/edit_legal_representative.html', args)

@login_required(login_url='login')
@read_write_permission_required(login_url='login')
@admin_required(login_url='login')
def delete_legal_representative(request, cpf_cnpj):
    return redirect('delete_legal_representative_confirmation', cpf_cnpj=cpf_cnpj)

@login_required(login_url='login')
@read_write_permission_required(login_url='login')
@admin_required(login_url='login')
def delete_legal_representative_confirmation(request, cpf_cnpj):
    applicant = Applicant.objects.get(cpf_cnpj=cpf_cnpj)
    legal_representative = LegalRepresentative.objects.get(applicant_represented=applicant)

    if request.method == 'POST':
        legal_representative.delete()
        return redirect('applicant_info', cpf_cnpj=cpf_cnpj)
    else:
        args = {'applicant': applicant, 'legal_representative': legal_representative}
        return render(request, 'applicants/delete_legal_representative_confirmation.html', args)

@login_required(login_url='login')
@read_write_permission_required(login_url='login')
def new_legal_representative(request, cpf_cnpj):
    applicant = Applicant.objects.get(cpf_cnpj=cpf_cnpj)

    if request.method == 'POST':
        form = LegalRepresentativeCreationForm(request.POST)
        if form.is_valid():
            legal_representative = form.save(commit=False)
            legal_representative.applicant_represented = applicant
            legal_representative.save()
            return redirect('applicant_info', cpf_cnpj=cpf_cnpj)

        args = {'form': form}
        return render(request, 'applicants/new_legal_representative.html', args)
    else:
        form = LegalRepresentativeCreationForm()

        args = {'form': form}
        return render(request, 'applicants/new_legal_representative.html', args)

@login_required(login_url='login')
@read_write_permission_required(login_url='login')
@admin_required(login_url='login')
def delete_applicant(request, cpf_cnpj):
    return redirect('delete_applicant_confirmation', cpf_cnpj=cpf_cnpj)

@login_required(login_url='login')
@read_write_permission_required(login_url='login')
@admin_required(login_url='login')
def delete_applicant_confirmation(request, cpf_cnpj):
    applicant = Applicant.objects.get(cpf_cnpj=cpf_cnpj)

    if request.method == 'POST':
        applicant_path = os.path.join(reports_path, applicant.cpf_cnpj)

        if applicant.cpf_cnpj in os.listdir(reports_path):
            shutil.rmtree(applicant_path)

        applicant.delete()
        return redirect('list_applicants')
    else:
        return render(request, 'applicants/delete_applicant_confirmation.html', {'applicant': applicant})

def create_legal_representative_form_from_post_request(post):
    args = {
        'name': post.get('representative_name', ''),
        'cpf': post.get('representative_cpf', ''),
        'email': post.get('representative_email', ''),
        'phone': post.get('representative_phone', ''),
        'cellphone': post.get('representative_cellphone', ''),
    }
    return LegalRepresentativeCreationForm(args)

@login_required(login_url='login')
@read_write_permission_required(login_url='login')
def new_applicant(request):
    if request.method == 'POST':
        form = ApplicantCreationForm(request.POST)
        form2 = create_legal_representative_form_from_post_request(request.POST)
        if form.is_valid():
            form.save()
            if form.cleaned_data['has_representative'] == True:
                if form2.is_valid():
                    applicant = Applicant.objects.get(cpf_cnpj=request.POST['cpf_cnpj'])
                    legal_representative = form2.save(commit=False)
                    legal_representative.applicant_represented = applicant
                    legal_representative.save()
                    return redirect('new_certification', cpf_cnpj=request.POST['cpf_cnpj'])
                else:
                    Applicant.objects.get(cpf_cnpj=request.POST['cpf_cnpj']).delete()
            else:
                return redirect('new_certification', cpf_cnpj=request.POST['cpf_cnpj'])

        args = {'form': form, 'form2': form2}
        return render(request, 'applicants/new_applicant.html', args)
    else:
        form = ApplicantCreationForm()
        form2 = LegalRepresentativeCreationForm()

        args = {'form': form, 'form2': form2}
        return render(request, 'applicants/new_applicant.html', args)

@login_required(login_url='login')
def list_applicants(request):
    applicants = Applicant.objects.all()
    return render(request, 'applicants/list_applicants.html', {'applicants': applicants})

@login_required(login_url='login')
def search_applicant(request):
    search_term = request.GET.get('search_for', '')
    where = request.GET.get('in', '')
    if where == 'name':
        applicants = Applicant.objects.filter(name__icontains=search_term)
        where = 'Nome/Razão Social'
    elif where == 'cpf_cnpj':
        applicants = Applicant.objects.filter(cpf_cnpj__icontains=search_term)
        where = 'CPF/CNPJ'
    elif where == 'email':
        applicants = Applicant.objects.filter(email__icontains=search_term)
        where = 'Email'
    elif where == 'phone':
        applicants = Applicant.objects.filter(phone__icontains=search_term)
        where = 'Telefone'
    elif where == 'legal_representative':
        applicants = Applicant.objects.filter(legal_representative__name__icontains=search_term)
        where = 'Representante Legal'
    else:
        applicants = Applicant.objects.all()
        where = 'indefinido'
    args = {'search_term': search_term, 'where': where, 'applicants': applicants}
    return render(request, 'applicants/search_applicant.html', args)
