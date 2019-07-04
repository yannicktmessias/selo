from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as user_admin

from django.utils.translation import gettext, gettext_lazy as _

from .forms import UserCreationForm, UserChangeForm
from .models import User


class UserAdmin(user_admin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    
    fieldsets = (
        (None, {'fields': ('name', 'rf', 'password')}),
        (_('Personal info'), {'fields': ('email', 'cpf', 'rg')}),
        (_('Permissions'), {
            'fields': ('is_admin', 'permissions', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'rf', 'email', 'cpf', 'rg', 'is_admin', 'permissions', 'password1', 'password2'),
        }),
    )
    list_display = ('name', 'rf', 'email', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups',)
    search_fields = ('name', 'rf', 'email',)
    ordering = ('name',)


admin.site.register(User, UserAdmin)