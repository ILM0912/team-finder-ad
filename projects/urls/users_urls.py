from django.urls import path

from ..views import users_views

app_name = 'users'

urlpatterns = [
    path(
        'list/',
        users_views.participants_list,
        name='participants_list'
    ),
    path(
        '<int:user_id>/',
        users_views.user_details,
        name='user_details'
    ),
    path(
        'register/',
        users_views.register_user,
        name='register'
    ),
    path(
        'login/',
        users_views.login_user,
        name='login'
    ),
    path(
        'logout/',
        users_views.logout_user,
        name='logout'
    ),
    path(
        'change-password/',
        users_views.change_password,
        name='change-password'
    ),
    path(
        'edit-profile/',
        users_views.edit_profile,
        name='edit-profile'
    ),
]
