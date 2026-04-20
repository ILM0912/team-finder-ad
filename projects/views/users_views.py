
from django.shortcuts import render

from ..models import User


USER_FILTERS = [
    'owners-of-favorite-projects',
    'owners-of-participating-projects',
    'interested-in-my-projects',
    'participants-of-my-projects',
]


def participants_list(request):
    participants = User.objects.all()
    active_filter = request.GET.get('filter')

    if request.user.is_authenticated and active_filter in USER_FILTERS:

        if active_filter == 'owners-of-favorite-projects':
            participants = User.objects.filter(
                owned_projects__in=request.user.favorites.all()
            ).distinct()

        elif active_filter == 'owners-of-participating-projects':
            participants = User.objects.filter(
                owned_projects__participants=request.user
            ).distinct()

        elif active_filter == 'interested-in-my-projects':
            participants = User.objects.filter(
                favorites__owner=request.user
            ).distinct()

        elif active_filter == 'participants-of-my-projects':
            participants = User.objects.filter(
                participated_projects__owner=request.user
            ).exclude(id=request.user.id).distinct()

    context = {
        'participants': participants,
        'active_filter': active_filter,
    }
    return render(request, 'users/participants.html', context)
