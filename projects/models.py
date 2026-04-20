from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .validators import validate_github_profile, validate_github_repo


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Поле email обязательно')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Суперпользователь должен иметь is_staff=True'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Суперпользователь должен иметь is_superuser=True'
            )

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=124)
    surname = models.CharField(max_length=124)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    phone = models.CharField(
        max_length=12,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^(\+7|8)\d{10}$',
                message=(
                    "Номер должен быть в формате"
                    "8XXXXXXXXXX или +7XXXXXXXXXX"
                )
            )
        ]
    )
    github_url = models.URLField(
        blank=True,
        validators=[validate_github_profile]
    )
    about = models.TextField(blank=True, max_length=256)
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


class Project(models.Model):
    STATUS_CHOICES = [('open', 'Open'), ('closed', 'Closed')]

    name = models.CharField(max_length=200, verbose_name='Название проекта')
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
        max_length=6,
        choices=STATUS_CHOICES,
        default='open',
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

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
