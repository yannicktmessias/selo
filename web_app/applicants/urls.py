from django.urls import path

from . import views

urlpatterns = [
    path('<slug:cpf_cnpj>/', views.applicant_info, name='applicant_info'),
    path('<slug:cpf_cnpj>/editar/', views.edit_applicant, name='edit_applicant'),
    path('<slug:cpf_cnpj>/editar_representante_legal', views.edit_legal_representative, name='edit_legal_representative'),
    path('<slug:cpf_cnpj>/excluir_representante_legal', views.delete_legal_representative, name='delete_legal_representative'),
    path('<slug:cpf_cnpj>/confirmar_excluir_representante_legal', views.delete_legal_representative_confirmation, name='delete_legal_representative_confirmation'),
    path('<slug:cpf_cnpj>/novo_representante_legal', views.new_legal_representative, name='new_legal_representative'),
    path('<slug:cpf_cnpj>/excluir/', views.delete_applicant, name='delete_applicant'),
    path('<slug:cpf_cnpj>/confirmar_excluir/', views.delete_applicant_confirmation, name='delete_applicant_confirmation'),
    path('novo/', views.new_applicant, name='new_applicant'),
    path('todos/', views.list_applicants, name='list_applicants'),
    path('procurar/', views.search_applicant, name='search_applicant'),
]
