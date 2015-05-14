# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from inviMarket.forms import TradeForm, CommentsForm
from inviMarket.models import Trade, Notification
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _

@login_required
def propose(request, receptor_id):
    """
    Display the trade form and store the trade proposal in
    :model:`inviMarket.Trade`, related to :model:`auth.User`,
    :model:`inviMarket.Request` and :model:`inviMarket.Offer`.

    **Context**

    ``request_form``
      An instance of the trade form containing the request choices.

    ``offer_form``
      An instance of the trade form containing the offer choices.

    ``comments_form``
      An instance of the comments form containing additional comments.

    ``error``
      A string varaible used to inform the user about any error.

    **Template:**

    :template:`inviMarket/propose.html`

    """
    request_form = offer_form = comments_form = error = None
    proposer = request.user
    receptor = get_object_or_404(
        User.objects.prefetch_related('profile__partners'), pk=receptor_id)
    # Count proposer's pending proposals
    proposer_trades = proposer.proposed_trades.filter(accepted=False).count()
    proposer_trades += proposer.received_trades.filter(accepted=False).count()
    # Count receptor's pending proposals
    receptor_trades = receptor.proposed_trades.filter(accepted=False).count()
    receptor_trades += receptor.received_trades.filter(accepted=False).count()
    # Check existing pending trade and maximum number of total pending trades
    if proposer.proposed_trades.filter(receptor=receptor,
                                       accepted=False).exists():
        error = _("You have already made the user a trade proposal.")
    elif proposer_trades >= settings.MAX_TRADES:
        error = _("You have reached the maximum number of pending proposals.")
    elif receptor_trades >= settings.MAX_TRADES:
        error = _("The user have reached the maximum number of pending "
                  "proposals.")
    else:
        proposer_offers = proposer.profile.get_offers()
        receptor_offers = receptor.profile.get_offers()
        proposer_requests = proposer.profile.get_requests()
        receptor_requests = receptor.profile.get_requests()
        partners = (receptor.profile.partners.filter(
                        pk=proposer.pk).exists() and
                    proposer.profile.partners.filter(
                        pk=receptor.pk).exists())
        # Exclude protected sites if the users are not partners
        if not partners:
            proposer_offers = proposer_offers.exclude(website__protected=True)
            receptor_offers = receptor_offers.exclude(website__protected=True)
            proposer_requests = proposer_requests.exclude(
                website__protected=True)
            receptor_requests = receptor_requests.exclude(
                website__protected=True)
        # Prepare sites lists for the form
        offer_choices = list()
        offer_label = ''
        for o in proposer_offers:
            # Get offer-request coincidences
            for c in (r for r in receptor_requests if o.website == r.website):
                if c.website.logo:
                    img = '<img alt="Logo" src="' + c.website.logo.url + '"/>'
                else:
                    img = ""
                o_label = img + c.website.name
                offer_choices.append((c.website.pk, mark_safe(o_label)))
        # Same for the requests
        request_choices = list()
        request_label = ''
        for r in proposer_requests:
            for c in (o for o in receptor_offers if o.website == r.website):
                if c.website.logo:
                    img = '<img alt="Logo" src="' + c.website.logo.url + '"/>'
                else:
                    img = ""
                if c.to_donate > 0:
                    r_label = img + c.website.name + ' <sup>(*)</sup>'
                else:
                    r_label = img + c.website.name
                request_choices.append((c.website.pk, mark_safe(r_label)))
        if request.method == 'POST':
            request_form = TradeForm(request_choices, request_label,
                                     request.POST, prefix='request')
            offer_form = TradeForm(offer_choices, offer_label,
                                   request.POST, prefix='offer')
            comments_form = CommentsForm(request.POST)
            if (request_form.is_valid() and offer_form.is_valid() and
                    comments_form.is_valid()):
                offers = offer_form.cleaned_data['sites']
                requests = request_form.cleaned_data['sites']
                comments = comments_form.cleaned_data['comments']
                if len(requests) == 0 and len(offers) == 0:
                    error = _("You have not selected any request or offer.")
                else:
                    # Lock the users to minimize concurrency problems
                    if not proposer.profile.lock_perm():
                        error = _("Some requests/offers have changed. Reload "
                                  "andtry again.")
                    if not receptor.profile.lock_perm():
                        error = _("Some requests/offers have changed. Reload "
                                  "and try again.")
                        proposer.profile.unlock()
                    if not error:
                        # Create a new trade object
                        trade = Trade(proposer=proposer, receptor=receptor)
                        trade.save()
                        # Add the selected requests/offers to the trade proposal
                        for offer in offers:
                            try:
                                o = proposer.profile.get_offers().get(
                                    website=offer)
                                r = receptor.profile.get_requests().get(
                                    website=offer)
                                trade.offers.add(o)
                                trade.requests.add(r)
                            except ObjectDoesNotExist:
                                error = _("Some offers/requests have changed. "
                                          "Reload and try again.")
                                break
                        for req in requests:
                            try:
                                o = receptor.profile.get_offers().get(
                                    website=req)
                                r = proposer.profile.get_requests().get(
                                    website=req)
                                if len(offers) == 0 and o.to_donate == 0:
                                    error = _("Donations not available for the "
                                              "selected request.")
                                    break
                                trade.offers.add(o)
                                trade.requests.add(r)
                            except ObjectDoesNotExist:
                                error = _("Some offers/requests have changed. "
                                          "Reload and try again.")
                                break
                        if error:
                            trade.requests.clear()
                            trade.offers.clear()
                            trade.delete()
                            proposer.profile.unlock()
                            receptor.profile.unlock()
                        else:
                            trade.comments = comments
                            trade.save()
                            # Check if the user is modifying a received proposal
                            try:
                                old_trade = receptor.proposed_trades.get(
                                    receptor=proposer.id, accepted=False)
                                old_trade.requests.clear()
                                old_trade.offers.clear()
                                old_trade.delete()
                                proposer.notification_set.filter(code=10,
                                    sender=receptor).delete()
                            except ObjectDoesNotExist:
                                pass
                            # Send a notification to the receptor
                            url = ('http://' + settings.DOMAIN +
                                   reverse('trade' ,
                                           kwargs={'trade_id': trade.id}))
                            notification = Notification(user=receptor,
                                                        sender=proposer,
                                                        code=10, url=url)
                            notification.save()
                            # Send a notification email as well
                            if receptor.profile.notify:
                                text = render_to_string('email/proposal.txt',
                                    {'name': receptor.first_name,
                                     'proposer': proposer,
                                     'trade': trade,
                                     'domain': settings.DOMAIN})
                                html = render_to_string('email/proposal.html',
                                    {'name': receptor.first_name,
                                     'proposer': proposer,
                                     'trade': trade,
                                     'domain': settings.DOMAIN})
                                subject = "Trade proposal"
                                send_mail(subject, text,
                                          "inviMarket <no-reply@inviMarket.com>",
                                          [receptor.email],
                                          html_message=html,
                                          fail_silently=False)
                            proposer.profile.unlock()
                            receptor.profile.unlock()
                            return redirect('proposal_submitted')
        else:
            # Check if modifying a received proposal and get initial values
            try:
                trade = receptor.proposed_trades.get(receptor=proposer,
                                                     accepted=False)
                initial_requests = list()
                for r in trade.get_receptor_requests():
                    initial_requests.append(r.website.pk)
                initial_offers = list()
                for o in trade.get_receptor_offers():
                    initial_offers.append(o.website.pk)
                request_form = TradeForm(request_choices, request_label,
                    prefix='request', initial={'sites': initial_requests})
                offer_form = TradeForm(offer_choices, offer_label,
                    prefix='offer', initial={'sites': initial_offers})
            except ObjectDoesNotExist:
                request_form = TradeForm(request_choices, request_label,
                    prefix='request')
                offer_form = TradeForm(offer_choices, offer_label,
                    prefix='offer')
            comments_form = CommentsForm()
    return render(request, 'propose.html', {
        'request_form': request_form,
        'offer_form': offer_form,
        'comments_form': comments_form,
        'error': error,
        'receptor': receptor,
        })
