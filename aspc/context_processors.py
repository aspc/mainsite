from django.contrib.sites.models import Site, RequestSite
import re

def site(request):
    port_string = request.META.get('SERVER_PORT')
    site_info = {
        'protocol': request.is_secure() and 'https' or 'http',
        'port': port_string if port_string != "80" else None
    }
    if Site._meta.installed:
        site_info['domain'] = Site.objects.get_current().domain
    else:
        site_info['domain'] = RequestSite(request).domain
    return site_info

def absolute_uri(request):
    return {
        'absolute_uri': request.build_absolute_uri()
    }

def is_mobile(request):
    user_agent = request.META.get('HTTP_USER_AGENT') or request.META.get('HTTP_AGENT')

    return {
        'is_mobile': bool(re.search(
                'Android|BlackBerry|iPhone|iPad|iPod|Opera Mini|IEMobile|SymbianOS|Windows Phone|Mobile',
                user_agent,
                re.IGNORECASE
            )) if user_agent else False
    }