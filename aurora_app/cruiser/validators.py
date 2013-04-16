from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_presence(value):
    """Validate presence of value"""
    if any([value is None, str(value).strip() == '']):
        raise ValidationError(_('Value is blank.'))
