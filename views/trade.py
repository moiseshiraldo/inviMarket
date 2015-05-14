# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from inviMarket.models import Trade, Notification
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _

@login_required
def trade(request, trade_id):
    """
    Display the trade :model:`inviMarket.Trade` passed by argument and the
    accept/reject form.

    **Context**

    ``error``
      A string variable used to inform the user.

    ``trade``
      An object containing the trade information.

    **Template:**

    :template:`inviMarket/trade.html`

    """
    user = request.user
    trade = get_object_or_404(
        Trade.objects.select_related('proposer', 'receptor'), pk=trade_id)
    proposer = trade.proposer
    receptor = trade.receptor
    error = None
    # Only the receptor can check the trade details, and the proposer once
    # the trade is accepted
    if user != receptor and (user != proposer or trade.accepted == False):
        return redirect('index')
    if trade.accepted == True and user == proposer:
        # Delete the accepted trade proposal notification
        proposer.notification_set.filter(code=30, sender=receptor).delete()
    if request.method == 'POST' and user == receptor:
        # Only the trade receptor can change the proposal status
        if 'Accept_proposal' in request.POST and trade.accepted == False:
            # Lock the users to avoid concurrency problems
            if not proposer.profile.lock_perm():
                error = _("Some requests/offers status have changed. Reload "
                          "and try again.")
            if not receptor.profile.lock_perm():
                error = _("Some requests/offers status have changed. Reload "
                          "and try again.")
                proposer.profile.unlock()
            if not error:
                trade.accepted = True
                trade.save()
                for req in trade.requests.all().prefetch_related('trade_set'):
                    req.traded = True
                    req.save()
                    # Clear pending trades related to the traded invites
                    trades = req.trade_set.filter(
                        accepted=False).select_related('receptor', 'proposer')
                    for t in trades:
                        t.requests.clear()
                        t.offers.clear()
                        t.delete()
                        t.receptor.notification_set.filter(
                            code=10, sender=t.proposer).delete()
                for offer in trade.offers.all().prefetch_related('trade_set'):
                    if offer.number == offer.to_donate or trade.donation:
                        offer.to_donate -= 1
                    offer.number -=1
                    offer.save()
                    # Clear pending trades related to the traded invites
                    if offer.number == 0:
                        trades = offer.trade_set.filter(
                          accepted=False).select_related('receptor', 'proposer')
                        for t in trades:
                            t.requests.clear()
                            t.offers.clear()
                            t.delete()
                            t.receptor.notification_set.filter(
                                code=10, sender=t.proposer).delete()
                # Send a notification to the proposer
                url = ('http://' + settings.DOMAIN +
                       reverse('trade', kwargs={'trade_id': trade.pk}))
                notification = Notification(user=proposer, sender=receptor,
                                            code=30, url=url)
                notification.save()
                receptor.notification_set.filter(code=10,
                    sender=proposer).delete()
                # Send a notification email as well
                if receptor.profile.notify:
                    text = render_to_string('email/trade.txt', {
                        'name': proposer.first_name,
                        'receptor': receptor,
                        'trade': trade,
                        'domain': settings.DOMAIN,
                        })
                    html = render_to_string('email/trade.html', {
                        'name': proposer.first_name,
                        'receptor': receptor,
                        'trade': trade,
                        'domain': settings.DOMAIN,
                        })
                    subject = "Accepted proposal"
                    send_mail(
                        subject, text,
                        "inviMarket <no-reply@inviMarket.com>",
                        [proposer.email],
                        html_message=html,
                        fail_silently=False
                        )
                proposer.profile.unlock()
                receptor.profile.unlock()
                return redirect('trade_accepted')
        if 'Reject_proposal' in request.POST:
            if not proposer.profile.lock_perm():
              error = _("Some requests/offers status have changed. Reload "
                        "and try again.")
            if not receptor.profile.lock_perm():
              error = _("Some requests/offers status have changed. Reload "
                        "and try again.")
              proposer.profile.unlock()
            if not error:
                trade.requests.clear()
                trade.offers.clear()
                trade.delete()
                receptor.notification_set.filter(
                    code=10, sender=proposer).delete()
                proposer.profile.unlock()
                receptor.profile.unlock()
                return redirect('trade_rejected')
    return render(request, 'trade.html', {
        'trade': trade,
        'error': error,
        'sending_deadline': settings.SENDING_DEADLINE,
        'complaint_deadline': settings.COMPLAINT_DEADLINE
        })