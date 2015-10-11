from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^requests/', include('apps.requests.urls')),
    url(r'^', include('apps.hello.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls'))
)


if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
                             {'document_root': settings.MEDIA_ROOT}))
