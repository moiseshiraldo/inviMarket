# -*- coding: utf-8 -*-
from functools import wraps
from django.views.decorators.cache import cache_page
from django.utils.decorators import available_attrs

def cache_on_auth(timeout):
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if user.is_authenticated() and user.profile.count_notifications():
                return view_func(request, *args, **kwargs)
            else:
                return cache_page(timeout,
                    key_prefix="_auth_%s_" % request.user.is_authenticated())(
                        view_func)(request, *args, **kwargs)
        return _wrapped_view
    return decorator