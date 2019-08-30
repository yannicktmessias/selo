from django.db import models
from applicants.models import Applicant

from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from accounts.validators import NumericValidator

class Certification(models.Model):
#   SEI Process
    applicant = models.ForeignKey(
        Applicant, 
        on_delete=models.CASCADE,
    )
    sei_number = models.CharField(
        _('SEI process number'),
        max_length = 20,
        unique = True,
        help_text = _('Required.'),
        validators = [NumericValidator()],
        error_messages={
            'unique': _("A certification with that SEI process number already exists."),
        },
    )
    sei_protocol = models.CharField(
        _('SEI process protocol'),
        max_length = 20,
        help_text = _('Required.'),
    )
    domain = models.CharField(
        _('domain'),
        max_length = 100,
        help_text = _('Required.'),
    )
    PUBLIC = 'PB'
    PRIVATE = 'PV'
    NATURE = [
        (PUBLIC, _('public')),
        (PRIVATE, _('private')),
    ]
    sei_nature = models.CharField(
        _('SEI process nature'),
        max_length=2,
        choices=NATURE,
        default=PRIVATE,
    )
    request_date = models.DateTimeField(
        _('request date'),
    )
    refusal_date = models.DateTimeField(
        _('refusal date'),
    )
#   Certification
    code = models.CharField(
        _('code'),
        max_length = 20,
        help_text = _('Required.'),
        validators = [NumericValidator()],
    )
    grant_date = models.DateTimeField(
        _('grant date'),
    )
    renewal_date = models.DateTimeField(
        _('renewal date'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this certification should be treated as active. '
            'Unselect this instead of deleting certifications.'
        ),
    )

class Page(models.Model):
    certification = models.ForeignKey(
        Certification, 
        on_delete=models.CASCADE,
    )
    url = models.CharField(
        _('URL'),
        max_length = 100,
        unique = True,
        primary_key=True,
        help_text = _('Required.'),
        error_messages={
            'unique': _("A page with that URL already exists."),
        },
    )
    is_homepage = models.BooleanField(
        _('homepage'),
        default=False,
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this page should be treated as active. '
            'Unselect this instead of deleting pages.'
        ),
    )