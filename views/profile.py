# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

@login_required
def profile(request, user_id=None):
    """
    Display the :model:`inviMarket.Profile` of the :model:`auth.User` passed by
    argument, or by default the own one.

    **Context**

    ``u``
      An instance of :model:`auth.User`.

    **Template:**

    :template:`inviMarket/profile.html`

    """
    if user_id is not None:
        user = get_object_or_404(User.objects.select_related('profile'),
            pk=user_id)
    else:
        user = request.user
    return render(request, 'profile.html', {'u': user})