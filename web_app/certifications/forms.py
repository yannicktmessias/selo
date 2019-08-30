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
            'sei_protocol',
            'code',
            'domain',
            'request_date',
            'refusal_date',
            'grant_date',
            'renewal_date',
            'sei_nature',
        )

class CertificationChangeForm(ModelForm):

    class Meta:
        model = Certification
        fields = (
            'sei_protocol',
            'domain',
            'request_date',
            'refusal_date',
            'grant_date',
            'renewal_date',
            'sei_nature',
        )

class PageCreationForm(ModelForm):

    class Meta:
        model = Page
        fields = (
            'url',
        )