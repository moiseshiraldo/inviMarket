# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils import translation
from django.utils.translation import ugettext as _

from inviMarket.models import User, Notification

@login_required
def add_partner(request, partner_id):
    """
    Add the :model:`auth.User` passed by argument to the partners list, and
    send a notification to the user if necessary.

    **Context**

    ``message``
      A string variable used to inform the user about the request.

    ``header``
      A string variable containing the message header.

    **Template:**

    :template:`inviMarket/message.html`

    """
    user = request.user
    partner = get_object_or_404(User.objects.select_related('profile'),
                                pk=partner_id, is_active=True)
    header = _("Partnership request")
    if user.profile.partners.filter(pk=partner_id).exists():
        message = _("The user is already your partner.")
    elif user.profile.partners.count() >= settings.MAX_PARTNERS:
        message = _("You have reached the maximum number of partners.")
    # Check if replying a partnership request
    elif partner.profile.partners.filter(pk=user.id).exists():
        user.profile.partners.add(partner)
        message = _("The user has been successfuly added to your partners "
                    "list.")
        user.notification_set.filter(code=20, sender=partner).delete()
    else:
        user.profile.partners.add(partner)
        # Send a notification to the user
        url = ('http://' + settings.DOMAIN +
               reverse('partners',kwargs={'partner_id': user.pk}))
        notification = Notification(user=partner, sender=user, code=20, url=url)
        notification.save()
        # Send a notification email as well
        if partner.profile.notify:
            cur_language = translation.get_language()
            try:
                translation.activate(partner.profile.lang)
                text = render_to_string('email/partnership.txt', {
                                        'name': partner.first_name,
                                        'user': user,
                                        'domain': settings.DOMAIN,
                                        })
                html = render_to_string('email/partnership.html', {
                                        'name': partner.first_name,
                                        'user': user,
                                        'domain': settings.DOMAIN,
                                        })
                subject = _("Partnership request")
                send_mail(subject, text,
                          "inviMarket <no-reply@inviMarket.com>",
                          [partner.email],
                          html_message=html,
                          fail_silently=False)
            finally:
                translation.activate(cur_language)
        message = _("The partnership request has been sended to the user.")
    return render(request, 'message.html', {
        'header': header,
        'message': message,
        })