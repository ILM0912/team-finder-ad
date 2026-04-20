from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.index_redirect, name='index'),
    path('projects/list/', views.project_list, name='project_list'),
    path(
        'projects/<int:project_id>/toggle-favorite/',
        views.toggle_favorite,
        name='toggle_favorite',
    ),
]
