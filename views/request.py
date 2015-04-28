# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from inviMarket.models import Website, Request
from django.db.models import Sum
from django.conf import settings
import random
from django.utils.translation import ugettext as _


def request(request, site_id):
    """
    Store an invite request in :model:`inviMarket.Request`, related to
    :model:`inviMarket.Website` and :model:`auth.User`, or get a random
    referral link if the passed argument is a referral site.

    **Context**

    ``error``
      A string variable containing any error message.

    ``site``
      An instance of the site.

    ``offer``
      A variable that contains a random referral offer.

    **Template:**

    :template:`inviMarket/request.html`

    """
    site = get_object_or_404(Website, pk=site_id)
    user = request.user
    chosen_offer = error = None
    if site.category == 'RE':
        # Get a random referral link from all the offered ones
        offers = site.offer_set.all().only('weight').order_by(
            '-weight')
        if offers:
            total_weight = offers.aggregate(Sum('weight'))['weight__sum']
            rnd = random.random()*total_weight
            for offer in offers:
                rnd -= offer.weight
                if rnd < 0:
                    chosen_offer = offer
                    break
    elif not request.user.is_authenticated():
        return redirect('login')
    # If not a referral site and no errors, store the request
    elif user.request_set.filter(website=site_id).exists():
        error = _("You have already requested an invite for this site.")
    elif user.request_set.filter(traded=False).count() >= settings.MAX_REQUESTS:
        error = _("You have reached the maximum number of simultaneous "
                  "requests.")
    else:
        r = Request(user=user, website=site)
        r.save()
    return render(request, 'request.html', {
        'error': error,
        'site': site,
        'offer': chosen_offer,
        })