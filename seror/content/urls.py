# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import PageView
from .views import TestView

urlpatterns = patterns ('',
    url(r'/notify', PageView.as_view(), name='page'),
    url(r'/test', TestView.as_view(), name='page'),

)