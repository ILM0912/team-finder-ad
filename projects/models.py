from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.urls import reverse

from .validators import validate_github_profile, validate_github_repo
from .utils import generate_avatar
from .managers import UserManager
from .constants import (
    ABOUT_MAX_LENGTH,
    NAME_MAX_LENGTH,
    PHONE_MAX_LENGTH,
    PROJECT_NAME_MAX_LENGTH,
    PROJECT_STATUS_CHOICES,
    PROJECT_STATUS_MAX_LENGTH,
    STATUS_OPEN,
    SURNAME_MAX_LENGTH,
    USER_AVATAR_UPLOAD_TO,
)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    name = models.CharField(max_length=NAME_MAX_LENGTH, verbose_name='Имя')
    surname = models.CharField(
        max_length=SURNAME_MAX_LENGTH,
        verbose_name='Фамилия'
    )
    avatar = models.ImageField(
        upload_to=USER_AVATAR_UPLOAD_TO,
        blank=True,
        verbose_name='Аватарка'
    )
    phone = models.CharField(
        max_length=PHONE_MAX_LENGTH,
        verbose_name='Телефон',
        validators=[
            RegexValidator(
                regex=r'^(\+7|8)\d{10}$',
                message=(
                    "Номер должен быть в формате "
                    "8XXXXXXXXXX или +7XXXXXXXXXX"
                )
            )
        ]
    )
    github_url = models.URLField(
        blank=True,
        validators=[validate_github_profile],
        verbose_name='GitHub'
    )
    about = models.TextField(
        blank=True,
        max_length=ABOUT_MAX_LENGTH,
        verbose_name='О себе'
    )
    favorites = models.ManyToManyField(
        'Project',
        related_name='interested_users',
        blank=True,
        verbose_name='Избранные проекты'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.avatar and self.name:
            avatar = generate_avatar(self.name[0]+self.surname[0])
            self.avatar.save(f"{self.email}_avatar.png", avatar, save=False)

        if self.phone:
            if self.phone.startswith('8'):
                self.phone = '+7' + self.phone[1:]
            exists = User.objects.filter(phone=self.phone)
            if self.pk:
                exists = exists.exclude(pk=self.pk)
            if exists.exists():
                raise ValidationError(
                    {'phone': 'Номер телефона уже используется'}
                )
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} {self.surname}'

    def get_absolute_url(self):
        return reverse('users:user_details', kwargs={'user_id': self.id})

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Project(models.Model):
    name = models.CharField(
        max_length=PROJECT_NAME_MAX_LENGTH,
        verbose_name='Название проекта'
    )
    description = models.TextField(blank=True, verbose_name='Описание проекта')
    owner = models.ForeignKey(
        User,
        related_name='owned_projects',
        on_delete=models.CASCADE,
        verbose_name='Автор проекта'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    github_url = models.URLField(
        blank=True,
        validators=[validate_github_repo],
        verbose_name='Ссылка на Github репозиторий'
    )
    status = models.CharField(
        max_length=PROJECT_STATUS_MAX_LENGTH,
        choices=PROJECT_STATUS_CHOICES,
        default=STATUS_OPEN,
        verbose_name='Статус проекта'
    )
    participants = models.ManyToManyField(
        'User',
        related_name='participated_projects',
        blank=True,
        verbose_name='Участники проекта'
    )

    @property
    def likes_count(self):
        return self.interested_users.count()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'projects:project_details',
            kwargs={'project_id': self.id}
        )

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        ordering = ["-created_at"]
