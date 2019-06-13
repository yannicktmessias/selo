from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail

from .validators import NumericValidator


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, name, rf, email, password, **extra_fields):
        """
        Create and save a user with the given name, rf, email, and password.
        """
        if not rf:
            raise ValueError('The given RF must be set')
        email = self.normalize_email(email)
        name = self.model.normalize_username(name)
        user = self.model(name=name, rf=rf, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, name, rf, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, rf, email, password, **extra_fields)

    def create_superuser(self, name, rf, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(name, rf, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(
        _('full name'),
        max_length = 100,
        help_text = _('Required.'),
    )
    rf = models.CharField(
        _('RF'),
        max_length = 30,
        unique = True,
        help_text = _('Required.'),
        validators = [NumericValidator],
        error_messages={
            'unique': _("A user with that RF already exists."),
        },
    )
    email = models.EmailField(
        _('email address'),
        help_text = _('Required.'),
        blank = True,
    )
    cpf = models.CharField(
        _('CPF'),
        max_length = 15,
        unique = True,
        help_text = _('Required.'),
        validators = [NumericValidator],
        error_messages={
            'unique': _("A user with that CPF already exists."),
        },
        blank = True,
    )
    rg = models.CharField(
        _('RG'),
        max_length = 15,
        unique = True,
        help_text = _('Required.'),
        validators = [NumericValidator],
        error_messages={
            'unique': _("A user with that RG already exists."),
        },
        blank = True,
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'rf'
    REQUIRED_FIELDS = ['name', 'email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        names = self.name.split()
        full_name = '%s %s' % (names[0], names[-1])
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.name.split()[0]

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.get_short_name()
