from django.shortcuts import render, get_object_or_404
from .models import PageLink

def page_link(request, slug):
    page = get_object_or_404(PageLink, slug=slug)
    menu_pages = PageLink.objects.order_by('menu_order')

    return render(request, 'coustom_pages/page_link.html', {
        'page': page,
        'menu_pages': menu_pages,
    })
