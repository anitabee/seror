# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import PageView, notify


urlpatterns = patterns ('',
    url(r'^test/$', PageView.as_view(), name='page'),
    url(r'^notify/$', notify, name='notify'),

)