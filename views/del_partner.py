# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from inviMarket.models import User
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _

@login_required
def del_partner(request, partner_id):
    """
    Delete the :model:`auth.User` passed by argument from the partners list.

    **Context**

    ``message``
      A string variable used to inform the user.

    **Template:**

    :template:`inviMarket/addpartner.html`

    """
    user = request.user
    partner = get_object_or_404(User.objects.select_related('profile'),
                                pk=partner_id)
    url = ('http://' + settings.DOMAIN +
           reverse('partners', kwargs={'partner_id': partner_id}))
    message = _("Ther user is not your partner.")
    if partner.profile.partners.filter(pk=user.id).exists():
        partner.profile.partners.remove(user)
        message = _("The partnership proposal has been rejected.")
        user.notification_set.filter(code=20, sender=partner).delete()
    if user.profile.partners.filter(pk=partner_id).exists():
        user.profile.partners.remove(partner)
        message = _("The user is no longer your partner.")
    return render(request, 'message.html', {'message': message})