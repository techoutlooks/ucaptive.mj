from django.utils.translation import ugettext_lazy as _


# ACCOUNTS_PHONE_NUMBER_REGEX = "r'^\+?[0-9 .-]{9,15}$'"
PHONE_NUMBER_REGEX = "^[0-9]{9}$"
PHONE_NUMBER_ERROR_MSG = _('Invalid! Guinea local numbers only. 9 digits and no +')


GENDER_CHOICES = (
    ('M', _('Man')),
    ('F', _('Woman'))
)