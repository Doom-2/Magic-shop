from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from rest_framework import serializers


def check_field_not_true(value):
    if value:
        raise ValidationError(
            'When creating only \'false\' value is allowed'
        )


class DomainBlackList(EmailValidator):
    def __init__(self, domains):
        super().__init__()
        if not isinstance(domains, list):
            domains = [domains]

        self.domains = domains

    def __call__(self, email):
        user_part, domain_part = email.rsplit('@', 1)
        if domain_part in self.domains:
            raise serializers.ValidationError(f"You can't register from domain {domain_part}. Try another one")
