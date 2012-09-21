from django.conf import settings
from django.conf.urls.defaults import *
from django.views.decorators.csrf import csrf_exempt

from tendenci.urls import urlpatterns as tendenci_urls

handler500 = 'tendenci.core.base.views.custom_error'

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = staticfiles_urlpatterns()

if not settings.USE_S3_STORAGE:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
        url(r'^themes/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.THEMES_DIR,
        }),
    )


@csrf_exempt
def deploy_view(request):
    from django.http import HttpResponse
    from subprocess import Popen

    Popen(['python', 'deploy.py'])
    response = HttpResponse("Deploy triggered.", content_type="text/plain")
    return response

urlpatterns += patterns('',
    url(r'^deploy/%s/$' % settings.SECRET_KEY, deploy_view)
    )

urlpatterns += tendenci_urls
