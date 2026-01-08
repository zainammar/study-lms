from .models import PageLink

def page_links(request):
    return {
        'page_links': PageLink.objects.all()
    }
