# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect

from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils import timezone
from django.utils.translation import ugettext as _

import hashlib
import datetime
import random

from inviMarket.models import Profile
from inviMarket.forms import RegisterForm

def register(request):
    """
    Display the user registration form and store the :model:`auth.User` and
    his :model:`inviMarket.Profile` in the database.

    **Context**

    ``form``
      An instace of the user registration form.

    ``error``
      A string variable containing any general error message.

    **Template:**

    :template:`inviMarket/register.html`

    """
    error = None
    if request.user.is_authenticated():
        return redirect('index')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if 'terms' not in request.POST:
            error= _("You must read and accept the terms and conditions.")
        elif form.is_valid():
            if form.cleaned_data['last_name'] != "":
                return redirect('confirm')
            new_user = form.save()
            # Create a random activation key and store it in the user profile
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.sha1(salt+new_user.email).hexdigest()
            key_expires = timezone.now() + datetime.timedelta(2)
            lang = request.LANGUAGE_CODE
            profile = Profile(user=new_user, activation_key=activation_key,
                key_expires=key_expires, lang=lang)
            profile.save()
            # Send the activation key to the user
            text = render_to_string('email/activation.txt',
                {'name': new_user.first_name,
                 'uidb64': urlsafe_base64_encode(force_bytes(new_user.id)),
                 'key': activation_key,
                 'domain': settings.DOMAIN,
                 })
            html = render_to_string('email/activation.html',
                {'name': new_user.first_name,
                 'uidb64': urlsafe_base64_encode(force_bytes(new_user.id)),
                 'key': activation_key,
                 'domain': settings.DOMAIN,
                 })
            subject = "Account activation"
            send_mail(subject, text, "inviMarket <no-reply@inviMarket.com>",
                [new_user.email], html_message=html,fail_silently=False)
            return redirect('confirm')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form, 'error': error})