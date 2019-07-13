import re

from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

@deconstructible
class NumericValidator(validators.RegexValidator):
    regex = r'^([\d]+)$'
#   message = _('This field only accept numbers.')
    message = 'Este campo aceita somente números.'
    flags = 0
