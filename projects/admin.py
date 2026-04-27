from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import User, Project


@admin.register(User)
class TeamFinderUserAdmin(UserAdmin):
    model = User

    list_display = (
        'avatar_preview', 'id', 'email', 'name', 'surname', 'is_staff'
    )
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

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="30" height="30" />',
                obj.avatar.url
            )
        return '—'

    avatar_preview.short_description = 'Аватарка'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'owner', 'status', 'created_at', 'participants_count'
    )

    def participants_count(self, obj):
        return obj.participants.count()
    
    participants_count.short_description = 'Кол-во участников'
