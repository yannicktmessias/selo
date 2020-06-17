from django.forms import CharField, Form, ModelForm

from applicants.models import Applicant
from .models import Certification, Page

class CertificationApplicantForm(Form):
    cpf_cnpj = CharField(
        label = 'CPF/CNPJ',
        max_length = 20,
    )

class CertificationCreationForm(ModelForm):

    class Meta:
        model = Certification
        fields = (
            'sei_number',
            'code',
            'domain',
            'request_date',
            'grant_date',
            'sei_nature',
        )

class CertificationChangeForm(ModelForm):

    class Meta:
        model = Certification
        fields = (
            'domain',
            'grant_date',
            'renewal_date',
        )

class PageCreationForm(ModelForm):

    class Meta:
        model = Page
        fields = (
            'url',
        )