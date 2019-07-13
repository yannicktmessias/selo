from django.db import models

from django.utils.translation import gettext_lazy as _

from accounts.validators import NumericValidator

class Applicant(models.Model):
    name = models.CharField(
        _('name'),
        max_length = 60,
        help_text = _('Required.'),
    )
    cpf_cnpj = models.CharField(
        _('CPF/CNPJ'),
        max_length = 20,
        unique = True,
        help_text = _('Required.'),
        validators = [NumericValidator()],
        error_messages={
            'unique': _("An applicant with that CPF/CNPJ already exists."),
        },
    )
    email = models.EmailField(
        _('email address'),
        help_text = _('Required.'),
    )
    phone = models.CharField(
        _('phone'),
        max_length = 20,
        help_text = _('Required.'),
    )
    cellphone = models.CharField(
        _('cellphone'),
        max_length = 20,
    )
    adress_name = models.CharField(
        _('adress name'),
        max_length = 60,
        help_text = _('Required.'),
    )
    adress_number = models.CharField(
        _('adress number'),
        max_length = 6,
        help_text = _('Required.'),
        validators = [NumericValidator()],
    )
    adress_complement = models.CharField(
        _('adress complement'),
        max_length = 30,
        help_text = _('Required.'),
    )
    adress_neighborhood = models.CharField(
        _('neighborhood'),
        max_length = 30,
        help_text = _('Required.'),
    )
    adress_city = models.CharField(
        _('city'),
        max_length = 30,
        help_text = _('Required.'),
    )
    adress_state = models.CharField(
        _('state'),
        max_length = 30,
        help_text = _('Required.'),
    )
    adress_cep = models.CharField(
        _('CEP'),
        max_length = 15,
        help_text = _('Required.'),
    )

    def __str__(self):
        return self.name

class LegalRepresentative(models.Model):
    name = models.CharField(
        _('full name'),
        max_length = 60,
        help_text = _('Required.'),
    )
    cpf = models.CharField(
        _('CPF'),
        max_length = 15,
        unique = True,
        help_text = _('Required.'),
        validators = [NumericValidator()],
        error_messages={
            'unique': _("A legal representative with that CPF already exists."),
        },
    )
    email = models.EmailField(
        _('email address'),
        help_text = _('Required.'),
    )
    phone = models.CharField(
        _('phone'),
        max_length = 20,
        help_text = _('Required.'),
    )
    cellphone = models.CharField(
        _('cellphone'),
        max_length = 20,
    )
    applicant_represented = models.OneToOneField(
        Applicant,
        on_delete = models.CASCADE,
        related_name = _('applicant_represented_by'),
    )

    def __str__(self):
        return self.name