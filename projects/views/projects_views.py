from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator

from ..models import Project
from ..forms import ProjectForm
from ..constants import STATUS_OPEN


def project_list(request):
    projects = (Project.objects
                .select_related('owner')
                .prefetch_related('participants')
                )
    paginator = Paginator(projects, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    template = 'projects/project_list.html'
    context = {'projects': page_obj}
    return render(request, template, context)


def project_details(request, project_id):
    project = get_object_or_404(
        Project.objects
        .select_related('owner')
        .prefetch_related('participants', 'interested_users'),
        id=project_id
    )
    template = 'projects/project-details.html'
    context = {'project': project}
    return render(request, template, context)


@login_required
def favorite_projects(request):
    projects = projects = (
        request.user.favorites
        .select_related('owner')
        .prefetch_related('participants', 'interested_users')
    )
    template = 'projects/favorite_projects.html'
    context = {'projects': projects}
    return render(request, template, context)


@login_required
@require_POST
def toggle_favorite(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    user = request.user
    if favorited := user.favorites.filter(id=project.id).exists():
        user.favorites.remove(project)
    else:
        user.favorites.add(project)
    return JsonResponse({
        'status': 'ok',
        'favorited': not favorited,
    })


@login_required
@require_POST
def complete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if project.owner != request.user or project.status != STATUS_OPEN:
        return JsonResponse({
            "status": "error",
            "message": "Не выполнены условия"
        })

    project.status = 'closed'
    project.save()
    return JsonResponse({
        "status": "ok",
        "project_status": "closed"
    })


@login_required
@require_POST
def toggle_participate(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if project.status != STATUS_OPEN:
        return JsonResponse({
            'status': 'error',
            'message': 'Проект уже закрыт!'
        })
    if project.owner == request.user:
        return JsonResponse({
            'status': 'error',
            'message': 'Нельзя покидать свой проект!'
        })

    if participant := project.participants.filter(id=request.user.id).exists():
        project.participants.remove(request.user)
    else:
        project.participants.add(request.user)

    return JsonResponse({
        'status': 'ok',
        'participant': not participant
    })


@login_required
def create_project(request):
    template = 'projects/create-project.html'
    form = ProjectForm(request.POST or None)
    context = {
        'form': form,
        'is_edit': False,
    }
    if form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        project.participants.add(request.user)
        return redirect('projects:project_details', project_id=project.id)
    return render(request, template, context)


@login_required
def edit_project(request, project_id):
    template = 'projects/create-project.html'
    project = get_object_or_404(Project, id=project_id)
    form = ProjectForm(request.POST or None, instance=project)
    context = {
        'form': form,
        'is_edit': True,
    }
    if form.is_valid():
        project = form.save()
        return redirect('projects:project_details', project_id=project.id)
    return render(request, template, context)
