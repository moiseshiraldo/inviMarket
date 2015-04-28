# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from inviMarket.forms import ChainForm
from inviMarket.models import Website, Chain, Link
import hashlib, random
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

@login_required
def chain(request, site_id):
    """
    Display the current referral chain details. If it doesn't exist, display the
    chain creation form and store the chain in the database. Related
    to :model:`inviMarket.Chain`.

    **Context**

    ``chain_form``
      An instance of the chain creation form.

    **Template:**

    :template:`inviMarket/chain.html`

    """
    site = get_object_or_404(Website.objects.only('name', 'logo'), pk=site_id)
    user = request.user
    chain_form = chain = None
    try:
        chain = Chain.objects.get(owner=user, website=site)
    except ObjectDoesNotExist:
        if request.method == 'POST':
            chain_form = ChainForm(request.POST)
            if chain_form.is_valid():
                chain = chain_form.save(commit=False)
                chain.owner = user
                chain.website = site
                salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
                chain.url_hash = hashlib.sha1(
                    salt+user.username+site.name).hexdigest()
                if user.offer_set.filter(website=site).exists():
                    chain.save()
                    link = Link(user=user, chain=chain,
                        counter=chain.jumps, active=True, last_link=True)
                    link.save()
                    return redirect('chain_created')
                else:
                    "You must offer a refferal link to the site first."
        else:
          chain_form = ChainForm()
    return render(request, 'chain.html', {
        'chain_form': chain_form,
        'chain': chain,
        'site': site,
        })