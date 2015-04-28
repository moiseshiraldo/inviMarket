# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def del_profile(request):
    """
    Delete de user profile :model:`inviMarket.Profile`.

    **Template:**

    :template:`inviMarket/del_profile.html`

    """
    user = request.user
    if request.method == 'POST':
        # Delete the profile completely if selected
        if 'delete' in request.POST:
            user.profile.avatar.delete()
            for profile in user.partners():
              profile.partners.remove(user)
            user.profile.partners.clear()
            user.profile.delete()
            user.email.delete()
            user.first_name.delete()
        # By default just set the user as inactive
        user.is_active = False
        return redirect('logout')
    return render(request, 'del_profile.html')