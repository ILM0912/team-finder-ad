from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from ..models import Project


def index_redirect(request):
    return redirect('projects:project_list')


def project_list(request):
    projects = Project.objects.all()
    template = 'projects/project_list.html'
    context = {'projects': projects}
    return render(request, template, context)


@login_required
def favorite_projects(request):
    projects = request.user.favorites.all()
    template = 'projects/favorite_projects.html'
    context = {'projects': projects}
    return render(request, template, context)


@login_required
@require_POST
def toggle_favorite(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    user = request.user
    if user.favorites.filter(id=project.id).exists():
        user.favorites.remove(project)
        favorited = False
    else:
        user.favorites.add(project)
        favorited = True
    return JsonResponse({
        'status': 'ok',
        'favorited': favorited,
    })
