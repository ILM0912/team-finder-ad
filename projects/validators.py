import re

from django.core.exceptions import ValidationError


def validate_github_profile(value):
    if not value:
        return
    if not re.match(r'^https://github\.com/[\w\-\.]+/?$', value):
        raise ValidationError(
            'Ссылка должна быть на GitHub профиль '
            '(https://github.com/username)'
        )


def validate_github_repo(value):
    if not value:
        return
    if not re.match(r'^https://github\.com/[\w\-\.]+/[\w\-\.]+/?$', value):
        raise ValidationError(
            'Ссылка должна быть на GitHub репозиторий '
            '(https://github.com/username/repo)'
        )
