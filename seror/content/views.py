# -*- coding: utf-8 -*-
import os

from django.conf import settings
from django.views.generic import TemplateView
from django.http import Http404
# Create your views here.

class PageView(TemplateView):
    template_name = 'content/base.html'

    def get_context_data(self, **kwargs):
        context = super(PageView, self).get_context_data(**kwargs)

        return context

