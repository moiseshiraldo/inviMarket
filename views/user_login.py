# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.utils import translation
from django.utils.translation import ugettext as _

def user_login(request, next=None):
    """
    Display the login form and authenticate the user.

    **Context**

    ``error``
      A string variable containing any error message.

    ``next``
      The URL the user will be redirected to.

    **Template:**

    :template:`inviMarket/login.html`

    """
    error = nextURL = None
    if request.GET:
        nextURL = request.GET['next']
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                user_language = user.profile.lang
                translation.activate(user_language)
                if user_language:
                    request.session[
                        translation.LANGUAGE_SESSION_KEY] = user_language
                if nextURL:
                    return redirect(nextURL)
                else:
                    return redirect('index')
            else:
                error = _("Your account has not been activated yet.")
        else:
            error = _("Your username and password didn't match. Please "
                      "try again.")
    else:
        form = AuthenticationForm()
        form.fields['username'].label = _("Username/email")
    return render(request, 'login.html', {
        'form': form,
        'error': error,
        'next': nextURL
        })