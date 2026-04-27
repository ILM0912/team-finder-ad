from django.core.paginator import Paginator

from .constants import PAGE_SIZE


def paginate(request, queryset):

    paginator = Paginator(queryset, PAGE_SIZE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj
