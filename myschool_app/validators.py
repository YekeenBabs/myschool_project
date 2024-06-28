from django.core.exceptions import ValidationError # type: ignore
from django.utils.translation import gettext_lazy as _ # type: ignore
from datetime import date
from django.core.validators import RegexValidator # type: ignore


def validate_student_age(value):
    """
    Validates that a student's age is within a reasonable range.
    """
    current_year = date.today().year
    birth_year = current_year - value
    if not (5 <= value <= 25):
        raise ValidationError(
            _('Students must be between 5 and 25 years old.'),
            code='invalid_student_age'
        )


def validate_teacher_experience(value):
    """
    Validates that a teacher's experience is not more than their age.
    """
    if value > 60:
        raise ValidationError(
            _('Teachers cannot have more than 60 years of experience.'),
            code='invalid_teacher_experience'
        )


def validate_class_capacity(value):
    """
    Validates that a class capacity is within a reasonable range.
    """
    if not (10 <= value <= 50):
        raise ValidationError(
            _('Class capacity must be between 10 and 50.'),
            code='invalid_class_capacity'
        )


"""
# Other custom validators can be added as needed.
from django.db import models
from .validators import UnicodeUsernameValidator


class CustomUser(models.Model):
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    # Other fields and model logic here
"""


class UnicodeUsernameValidator(RegexValidator):
    """
    Validator for usernames that allows Unicode characters.
    """
    regex = r'^[\w.@+-]+$'
    message = _(
        'Enter a valid username. This value may contain only '
        'letters, numbers, and @/./+/-/_ characters.'
    )
    flags = 0


class CustomPasswordValidator:
    """
    Validator for custom password rules.
    """

    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(
                _("This password is too short. It must contain at least 8 characters."),
                code='password_too_short',
            )
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                _("This password must contain at least one digit."),
                code='password_no_digit',
            )
        if not any(char.isalpha() for char in password):
            raise ValidationError(
                _("This password must contain at least one letter."),
                code='password_no_letter',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 8 characters, one digit, and one letter."
        )
