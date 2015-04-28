# -*- coding: utf-8 -*-
from django.utils import timezone

class SetLastVisitMiddleware(object):
    def process_response(self, request, response):
        if response.status_code == 200 and request.user.is_authenticated():
            # Update last visit time after request finished processing.
            #request.user.profile.last_visit=timezone.now()
            #request.user.profile.save()
        return response