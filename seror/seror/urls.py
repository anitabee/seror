from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'seror.views.home', name='home'),
    url(r'test/', include('content.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
