from django.urls import path

from . import views

urlpatterns = [
    path('novo/', views.new_certification_applicant, name='new_certification_applicant'),
    path('novo/<slug:cpf_cnpj>/', views.new_certification, name='new_certification'),
    path('todos/', views.list_certifications, name='list_certifications'),
    path('procurar/', views.search_certification, name='search_certification'),
    path('<slug:sei_number>/', views.certification_info, name='certification_info'),
    path('<slug:sei_number>/<int:number_of_days>/', views.certification_info, name='certification_info_n'),
    path('<slug:sei_number>/relatorio/<int:page_id>/<path:date_time>/', views.report_show, name='report_show'),
    path('<slug:sei_number>/editar/', views.edit_certification, name='edit_certification'),
    path('<slug:sei_number>/excluir/', views.delete_certification, name='delete_certification'),
    path('<slug:sei_number>/confirmar_excluir/', views.delete_certification_confirmation, name='delete_certification_confirmation'),
    path('<slug:sei_number>/ativar/', views.activate_certification, name='activate_certification'),
    path('<slug:sei_number>/inativar/', views.inactivate_certification, name='inactivate_certification'),
    path('<slug:sei_number>/confirmar_inativar/', views.inactivate_certification_confirmation, name='inactivate_certification_confirmation'),
    path('<slug:sei_number>/relacao_de_paginas/', views.get_list_of_pages_document, name='get_list_of_pages_document'),
]
