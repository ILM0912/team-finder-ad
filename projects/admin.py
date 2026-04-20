from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Project


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ('id', 'email', 'name', 'surname', 'is_staff')
    ordering = ('id',)
    search_fields = ('email', 'name', 'surname')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личные данные', {
            'fields': (
                'name', 'surname', 'avatar', 'phone', 'github_url', 'about'
            )
        }),
        ('Избранное', {'fields': ('favorites',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'name', 'surname', 'phone', 'password1', 'password2'
            ),
        }),
    )

    filter_horizontal = ('groups', 'user_permissions', 'favorites')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'status', 'created_at')
