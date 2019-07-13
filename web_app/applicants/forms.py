from django.forms import ModelForm

from .models import Applicant, LegalRepresentative

ApplicantCreationForm(ModelForm):
	
	class Meta:
		model = Applicant
		fields = (
			'name',
			'cpf_cnpj',
			'email',
			'phone',
			'cellphone',
			'adress_name',
			'adress_number',
			'adress_complement',
			'adress_neighborhood',
			'adress_city',
			'adress_state',
			'adress_cep',
		)

ApplicantChangeForm(ModelForm):
	
	class Meta:
		model = Applicant
		fields = (
			'name',
			'email',
			'phone',
			'cellphone',
			'adress_name',
			'adress_number',
			'adress_complement',
			'adress_neighborhood',
			'adress_city',
			'adress_state',
			'adress_cep',
		)

LegalRepresentativeCreationForm(ModelForm):
	
	class Meta:
		model = LegalRepresentative
		fields = (
			'name',
			'cpf',
			'email',
			'phone',
			'cellphone',
			'applicant_represented',
		)

LegalRepresentativeChangeForm(ModelForm):
	
	class Meta:
		model = LegalRepresentative
		fields = (
			'name',
			'email',
			'phone',
			'cellphone',
		)	
