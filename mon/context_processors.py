from django.contrib.sites.models import Site
from django.conf import settings

def sites(request):
    if Site._meta.installed:
        site = Site.objects.get_current()
    else:
        site = RequestSite(request)
    return {'site': site.name}

def extra(request):
    return {'GOOGLE_API': getattr(settings, 'GOOGLE_API', None)}
