# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from inviMarket.models import Website
from inviMarket.forms import OfferForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django import forms
from django.utils import timezone
import datetime
import re
from django.utils.translation import ugettext as _

@login_required
def offer(request, site_id):
    """
    Store an invite offer in :model:`inviMarket.Offer`, related to
    :model:`inviMarket.Website` and :model:`auth.User`

    **Context**

    ``error``
      A variable string containing any general error message.

    ``site``
      The requested site.

    ``offer_form``
      An instance of the offer form.

    **Template:**

    :template:`inviMarket/offer.html`

    """
    site = get_object_or_404(Website, pk=site_id)
    user = request.user
    error = number = to_donate = None
    if request.method == 'POST':
        offer_form = OfferForm(request.POST)
        if site.category == 'RE':
            offer_form.fields['number'].widget = forms.HiddenInput()
            offer_form.fields['to_donate'].widget = forms.HiddenInput()
            offer_form.fields['number'].required = False
            offer_form.fields['to_donate'].required = False
        else:
            offer_form.fields['referral'].widget = forms.HiddenInput()
        if offer_form.is_valid():
            # Check if offering to a referral site and validate the link
            if site.category == 'RE':
                referral = offer_form.cleaned_data['referral']
                validator = re.compile(site.refvalidator)
                if referral == "":
                    user.offer_set.filter(website=site).delete()
                    return redirect('offer_deleted')
                elif validator.match(referral):
                    # Update the previous link or create a new offer
                    if user.offer_set.filter(website=site).exists():
                        o = user.offer_set.get(user=user, website=site)
                        o.referral=referral
                    else:
                        o = offer_form.save(commit=False)
                        o.user = user
                        o.website = site
                        o.number = 0
                        o.to_donate = 1
                        if user.link_set.filter(chain__website=site).exists():
                            link = user.link_set.get(chain__website=site)
                            link_expiration = link.date + datetime.timedelta(1)
                            if timezone.now() < link_expiration:
                                link.chain.add_link(link=link)
                    o.save()
                    return redirect('offer_submitted')
                else:
                    error = _("The referral link is not valid. Check it and "
                              "try again.")
            # Not referral site
            else:
                number = offer_form.cleaned_data['number']
                to_donate = offer_form.cleaned_data['to_donate']
                total_offers = user.offer_set.exclude(number=0).count()
                if not site.email_domain:
                    error = _("The 'mail domain' information is not available "
                              "yet for this site.")
                # Check if modifying an existing offer
                elif user.offer_set.filter(website=site).exists():
                    o = user.offer_set.get(website=site)
                    # Lock the user to minimize concurrency problems
                    if user.profile.lock_perm():
                        # If number equal to zero, delete the offer
                        if number == 0:
                            trades = o.trade_set.filter(accepted=False)
                            # Delete pending trades related to the offer
                            for trade in trades:
                                trade.request.clear()
                                trade.offer.clear()
                                trade.delete()
                            # Check if the offer is included in accepted trades
                            if o.trade_set.filter(accepted=True).count() == 0:
                                o.delete()
                            else:
                                o.number = 0
                                o.save()
                            user.profile.unlock()
                            return redirect('offer_deleted')
                        else:
                            # Update the existing offer
                            o.number = number
                            o.to_donate = to_donate
                            o.save()
                            user.profile.unlock()
                            return redirect('offer_submitted')
                    else:
                      error = _("Some error occurred. Reload and try again")
                elif total_offers >= settings.MAX_OFFERS:
                    error = _("You have reached the maximum number of "
                              "simultaneous offers.")
                else:
                    # Store the new offer
                    o = offer_form.save(commit=False)
                    o.user = user
                    o.website = site
                    o.save()
                    return redirect('offer_submitted')
    else:
        # If offer exists, get initial values
        if user.offer_set.filter(website=site).exists():
            o = user.offer_set.get(website=site)
            offer_form = OfferForm(instance=o)
        else:
            offer_form = OfferForm(initial={'number': 1, 'to_donate': 0})
        if site.category == 'RE':
            offer_form.fields['number'].widget = forms.HiddenInput()
            offer_form.fields['to_donate'].widget = forms.HiddenInput()
            offer_form.fields['number'].required = False
            offer_form.fields['to_donate'].required = False
        else:
            offer_form.fields['referral'].widget = forms.HiddenInput()
    return render(request, 'offer.html', {
        'offer_form': offer_form,
        'site':site,
        'error': error,
        })