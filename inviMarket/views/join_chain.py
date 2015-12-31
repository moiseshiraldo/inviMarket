# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _

from inviMarket.models import Chain, Link
from inviMarket.forms import PasswordForm

@login_required
def join_chain(request, cidb64, token):
    """
    Display the active referral link of the chain passed by argument.

    **Context**

    ``password_form``
      An instance of the password form.

    ``error``
      A string variable containing any error message.

    ``referral``
      The active referral link.

    ``chain``
      The related chain.

    **Template:**

    :template:`inviMarket/chain.html`

    """
    chain_id = force_text(urlsafe_base64_decode(cidb64))
    chain = get_object_or_404(Chain, pk=chain_id, url_hash=token)
    user = request.user
    error = form = referral = None
    if request.method == 'POST':
        # Check that the password is correct
        form = PasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            if password != chain.password:
                error = _("Invalid password.")
    elif chain.password:
        # If the chain has a password, display the form
        form = PasswordForm()
        return render(request, 'chain.html', {
            'password_form': form,
            'chain': chain
            })
    active_link = chain.get_active_link()
    try:
        link = Link.objects.get(user=user, chain=chain)
        # Check if the usear has already joined the chain
        if link.previous_link.exists() or chain.owner == user:
            error = _("You have already joined the referral chain.")
    except ObjectDoesNotExist:
        # Create the new link
        link = Link(user=user, chain=chain, counter=chain.jumps)
    if not error:
        # Get the active referral link
        referral = active_link.user.offer_set.get(
            website=chain.website).referral
        link.chain = chain
        link.counter = chain.jumps
        # Set the active link as the source of the new one
        link.source_link = active_link
        link.save()
    return render(request, 'chain.html', {
        'password_form': form,
        'error': error,
        'referral': referral,
        'chain': chain,
        })