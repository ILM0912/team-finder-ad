from django.urls import path

from .views import projects_views, users_views

app_name = 'projects'

urlpatterns = [
    path('', projects_views.index_redirect, name='index'),
    path('projects/list/', projects_views.project_list, name='project_list'),
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
]
