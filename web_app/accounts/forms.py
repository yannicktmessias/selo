from django.contrib.auth.forms import (
    UserCreationForm as user_creation_form,
    UserChangeForm as user_change_form,
    SetPasswordForm,
)

from .models import User


class UserCreationForm(user_creation_form):

    class Meta(user_creation_form):
        model = User
        fields = (
            'name',
            'rf',
            'email',
            'cpf',
            'rg',
            'permissions',
            'is_admin',
            'password1',
            'password2',
        )

class UserChangeForm(user_change_form):

    class Meta:
        model = User
        fields = (
            'name',
            'rf',
            'email',
            'cpf',
            'rg',
            'permissions',
            'is_admin',
            'is_active',
            'password',
        )