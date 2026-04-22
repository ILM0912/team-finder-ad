
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET

from ..models import User
from ..forms import RegisterForm, LoginForm, ChangePasswordForm


USER_FILTERS = [
    'owners-of-favorite-projects',
    'owners-of-participating-projects',
    'interested-in-my-projects',
    'participants-of-my-projects',
]


def user_details(request, user_id):
    user = get_object_or_404(User, id=user_id)
    template = 'users/user-details.html'
    context = {
        'user': user
    }
    return render(request, template, context)


def participants_list(request):
    active_filter = request.GET.get('filter')

    if request.user.is_authenticated and active_filter in USER_FILTERS:
        if active_filter == 'owners-of-favorite-projects':
            participants = User.objects.filter(
                owned_projects__in=request.user.favorites.all()
            ).distinct().order_by('id')

        elif active_filter == 'owners-of-participating-projects':
            participants = User.objects.filter(
                owned_projects__participants=request.user
            ).exclude(id=request.user.id).distinct().order_by('id')

        elif active_filter == 'interested-in-my-projects':
            participants = User.objects.filter(
                favorites__owner=request.user
            ).distinct().order_by('id')

        elif active_filter == 'participants-of-my-projects':
            participants = User.objects.filter(
                participated_projects__owner=request.user
            ).exclude(id=request.user.id).distinct().order_by('id')
    else:
        participants = User.objects.all().order_by('id')

    template = 'users/participants.html'
    context = {
        'participants': participants,
        'active_filter': active_filter,
    }
    return render(request, template, context)


def register_user(request):
    template = 'users/register.html'
    form = RegisterForm(request.POST or None)
    context = {'form': form}

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(request, user)
        return redirect('projects:project_list')

    return render(request, template, context)


def login_user(request):
    template = 'users/login.html'
    form = LoginForm(request.POST or None)
    context = {'form': form}
    if form.is_valid():
        user = authenticate(
            request,
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )

        if user is not None:
            login(request, user)
            return redirect('projects:project_list')
        form.add_error(None, 'Неверный email или пароль.')

    return render(request, template, context)


@login_required
def change_password(request):
    template = 'users/change_password.html'
    form = ChangePasswordForm(request.POST or None)
    context = {'form': form}

    if form.is_valid():
        old_password = form.cleaned_data['old_password']
        new_password1 = form.cleaned_data['new_password1']
        new_password2 = form.cleaned_data['new_password2']

        if not request.user.check_password(old_password):
            form.add_error('old_password', 'Неверный старый пароль')
        elif new_password1 != new_password2:
            form.add_error('new_password2', 'Пароли не совпадают')
        else:
            request.user.set_password(new_password1)
            request.user.save()
            login(request, request.user)
            return redirect('users:user_details', user_id=request.user.id)

    return render(request, template, context)


@login_required
@require_GET
def logout_user(request):
    logout(request)
    return redirect('projects:project_list')
