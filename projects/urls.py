from django.urls import path

from .views import projects_views, users_views

app_name = 'projects'

urlpatterns = [
    path('', projects_views.index_redirect, name='index'),
    path('projects/list/', projects_views.project_list, name='project_list'),
    path(
        'projects/<int:project_id>/',
        projects_views.project_details,
        name='project_details'
    ),
    path(
        'projects/<int:project_id>/complete/',
        projects_views.complete_project,
        name='complete_project'
    ),
    path(
        'projects/<int:project_id>/toggle-participate/',
        projects_views.toggle_participate,
        name='toggle_participate'
    ),
    path(
        'projects/favorites/',
        projects_views.favorite_projects,
        name='favorite_projects'
    ),
    path(
        'projects/<int:project_id>/toggle-favorite/',
        projects_views.toggle_favorite,
        name='toggle_favorite',
    ),
    path(
        'users/list/',
        users_views.participants_list,
        name='participants_list'
    ),
    path(
        'users/<int:user_id>/',
        users_views.user_details,
        name='user_details'
    ),
]
