# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.core.cache import cache

from inviMarket.models import Website, Offer, Request

def index(request):
    """
    Display the main page.

    **Context**

    ``popular``
      An object array containing the five most popular sites.

    ``new``
      An object array containing the five most recent sites.

    ``offers``
      An object array containing five random offers.

    ``requests``
      An object array containing five random requests.

    **Template:**

    :template:`inviMarket/market.html`

    """
    user = request.user
    # If first visit, redirect to the get started page
    first_visit = request.session.get('first_visit', None)
    if not user.is_authenticated() and first_visit != 'False':
        request.session['first_visit'] = 'False'
        return redirect('getstarted')
    lang = request.LANGUAGE_CODE
    cached = cache.get_many(['popular', 'offers', 'new', 'requests'])
    # Get most popular sites and filter by the user language
    popular_sites = cached.get('popular')
    if not popular_sites:
        popular_sites = Website.objects.filter(
            lang__in=('multi', lang, )).order_by('-popularity')[:5]
        cache.set('popular', popular_sites, 60*60)
    recent_offers = cached.get('offers')
    if not recent_offers:
        recent_offers = Offer.objects.exclude(number=0).order_by('?')[:5]
        cache.set('offers', recent_offers, 60*60)
    new_sites = cached.get('new')
    if not new_sites:
        new_sites = Website.objects.filter(
            lang__in=('multi', lang, )).order_by('-id')[:5]
        cache.set('new', new_sites, 60*60)
    recent_requests = cached.get('recent_requests')
    if not recent_requests:
        recent_requests = Request.objects.filter(traded=False).order_by('?')
        cache.set('requests', recent_requests, 60*60)
    return render(request, 'market.html', {
        'popular': popular_sites,
        'offers': recent_offers,
        'new': new_sites,
        'requests': recent_requests,
        })