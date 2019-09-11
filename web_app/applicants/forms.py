from django.forms import ModelForm, BooleanField

from .models import Applicant, LegalRepresentative

class ApplicantCreationForm(ModelForm):
    has_representative = BooleanField(required=False)
    
    class Meta:
        model = Applicant
        fields = (
            'name',
            'cpf_cnpj',
            'email',
            'phone',
            'cellphone',
            'address_name',
            'address_number',
            'address_complement',
            'address_neighborhood',
            'address_city',
            'address_state',
            'address_cep',
            'has_representative'
        )

class ApplicantChangeForm(ModelForm):
    
    class Meta:
        model = Applicant
        fields = (
            'name',
            'email',
            'phone',
            'cellphone',
            'address_name',
            'address_number',
            'address_complement',
            'address_neighborhood',
            'address_city',
            'address_state',
            'address_cep',
        )

class LegalRepresentativeCreationForm(ModelForm):
    
    class Meta:
        model = LegalRepresentative
        fields = (
            'name',
            'cpf',
            'email',
            'phone',
            'cellphone',
        )

class LegalRepresentativeChangeForm(ModelForm):
    
    class Meta:
        model = LegalRepresentative
        fields = (
            'name',
            'email',
            'phone',
            'cellphone',
        )
