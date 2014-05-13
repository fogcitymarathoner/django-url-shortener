from django.conf.urls import patterns, include, url

from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from urlweb.shortener.models import Link

#from django.views import generic
from shortener.views import LinkListView
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tiny.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),



    url(r'^$', LinkListView.as_view(), name='link-list'),
    url(r'^submit/$', 'shortener.views.submit'),
    url(r'^soap/$', 'shortener.views.soap'),
    url(r'^(?P<base62_id>\w+)$', 'shortener.views.follow'),
    url(r'^info/(?P<base62_id>\w+)$', 'shortener.views.info'),
    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
      {'document_root': settings.MEDIA_ROOT}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
      {'document_root': settings.MEDIA_ROOT}),
)
"""
"""
