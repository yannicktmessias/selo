from django.urls import path

from . import views

urlpatterns = [
    path('<int:cpf_cnpj>/', views.applicant_info, name='applicant_info'),
    path('<int:cpf_cnpj>/editar/', views.edit_applicant, name='edit_applicant'),
    path('<int:cpf_cnpj>/excluir/', views.delete_applicant, name='delete_applicant'),
    path('<int:cpf_cnpj>/confirmar_excluir/', views.delete_applicant_confirmation, name='delete_applicant_confirmation'),
    path('novo/', views.new_applicant, name='new_applicant'),
    path('todos/', views.list_applicants, name='list_applicants'),
    path('procurar/', views.search_applicant, name='search_applicant'),
]
