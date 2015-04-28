# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from inviMarket.models import Chain, Link
from inviMarket.forms import PasswordForm
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _

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

    **Template:**

    :template:`inviMarket/chain.html`

    """
    chain_id = force_text(urlsafe_base64_decode(cidb64))
    chain = get_object_or_404(Chain, pk=chain_id, url_hash=token)
    user = request.user
    error = form = referral = None
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            if password != chain.password:
                error = _("Invalid password.")
    elif chain.password:
        form = PasswordForm()
        return render(request, 'chain.html', {
            'password_form': form,
            'chain': chain
            })
    active_link = chain.get_active_link()
    try:
        link = Link.objects.get(user=user, chain=chain)
        if link.previous_link.exists() or chain.owner == user:
            error = _("You have already joined the referral chain.")
    except ObjectDoesNotExist:
        link = Link(user=user, chain=chain, counter=chain.jumps)
    if not error:
        referral = active_link.user.offer_set.get(
            website=chain.website).referral
        link.chain = chain
        link.counter = chain.jumps
        link.source_link = active_link
        link.save()
    return render(request, 'chain.html', {
        'password_form': form,
        'error': error,
        'referral': referral,
        'chain': chain,
        })