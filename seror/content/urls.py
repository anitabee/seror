# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import PageView

urlpatterns = patterns ('',
    url(r'', PageView.as_view(), name='page'),

)