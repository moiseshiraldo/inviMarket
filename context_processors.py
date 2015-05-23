# -*- coding: utf-8 -*-
from django.conf import settings
from django.template.loader import render_to_string

def analytics(request):
    """
    Returns Google Analytics code.

    """
    try:
        if not settings.DEBUG:
            return {'analytics_code': render_to_string("blocks/analytics.html",
                {'google_analytics_key': settings.GOOGLE_ANALYTICS_KEY }) }
        else:
            return { 'analytics_code': "" }
    except AttributeError:
        return { 'analytics_code': "" }