from django.contrib.auth.forms import (
    UserCreationForm as user_creation_form,
    UserChangeForm as user_change_form,
)

from .models import User


class UserCreationForm(user_creation_form):

    class Meta(user_creation_form):
        model = User
        fields = (
            'name',
            'rf',
            'email',
        )

class UserChangeForm(user_change_form):

    class Meta:
        model = User
        fields = (
            'name',
            'rf',
            'email',
        )