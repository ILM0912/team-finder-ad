from django.urls import path

from ..views import projects_views

app_name = 'projects'

urlpatterns = [
    path('list/', projects_views.project_list, name='project_list'),
    path(
        '<int:project_id>/',
        projects_views.project_details,
        name='project_details'
    ),
    path(
        '<int:project_id>/complete/',
        projects_views.complete_project,
        name='complete_project'
    ),
    path(
        '<int:project_id>/toggle-participate/',
        projects_views.toggle_participate,
        name='toggle_participate'
    ),
    path(
        'favorites/',
        projects_views.favorite_projects,
        name='favorite_projects'
    ),
    path(
        '<int:project_id>/toggle-favorite/',
        projects_views.toggle_favorite,
        name='toggle_favorite',
    ),
]
