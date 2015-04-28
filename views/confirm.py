from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils import timezone
#from django.core.files import File

def confirm(request, uidb64=None, key=None):
    """
    Display a confirmation message when the registration form is sended or
    activate the :model:`auth.User` account if the user id and activation key
    are passed as arguments.

    **Context**

    ``confirm``
      A boolean variable that indicates if the user has activated his account.

    **Template:**

    :template:`inviMarket/confirm.html`

    """
    if request.user.is_authenticated():
        return redirect('index')
    confirm = None
    if (uidb64 is not None) and (key is not None):
        user_id = force_text(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User.objects.select_related('profile'),
                                 pk=user_id)
        profile = user.profile
        now = timezone.now()
        if key == profile.activation_key and profile.key_expires > now:
            user.is_active = True
            user.save()
            confirm = True
        else:
            confirm = False
    return render(request, 'confirm.html', {'confirm': confirm})