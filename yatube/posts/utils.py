from django.core.paginator import Paginator

from .constants import POST_PER_PAGE


def show_paginator(request, objects_list):
    paginator = Paginator(objects_list.order_by('-pub_date'), POST_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
