from .models import PageLink

def menu_pages(request):
    pages = PageLink.objects.all().order_by('menu_order')  # order by menu_order
    return {'menu_pages': pages}
