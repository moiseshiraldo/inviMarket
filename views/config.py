# -*- coding: utf-8 -*-
from django.shortcuts import render
from inviMarket.forms import ConfigForm
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _

@login_required
def config(request):
    """
    Display the profile configuration form and update the
    :model:`inviMarket.Profile`.

    **Context**

    ``message``
      A string variable used to inform the user.

    ``config_form``
      An instance of the profile configuration form.

    **Template:**

    :template:`inviMarket/config.html`

    """
    message = None
    profile = request.user.profile
    if request.method == 'POST':
        config_form = ConfigForm(request.POST, request.FILES, instance=profile)
        if config_form.is_valid():
            config_form.save()
            message = _("Your profile has been successfuly updated.")
    else:
          config_form = ConfigForm(initial={
              'lang': profile.lang,
              'notify': profile.notify,
              'first_name': profile.user.first_name
              })
    return render(request, 'config.html', {
        'config_form': config_form,
        'message': message
        })