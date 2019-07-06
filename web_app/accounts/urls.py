from django.contrib.auth.views import LoginView, LogoutView
from . import views
from django.urls import path

urlpatterns = [
    path('login/', LoginView.as_view(template_name = 'accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', views.user_info, name='user_info'),
    path('<int:rf>/', views.user_info, name='user_info'),
    path('<int:rf>/editar/', views.edit_user, name='edit_user'),
    path('<int:rf>/excluir/', views.delete_user, name='delete_user'),
    path('novo/', views.new_user, name='new_user'),
    path('todos/', views.list_users, name='list_users'),
    path('procurar/', views.search_user, name='search_user'),
]