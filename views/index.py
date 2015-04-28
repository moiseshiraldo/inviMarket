# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from inviMarket.models import Website, Offer, Request
from django.db.models import Q

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
    first_visit = request.session.get('first_visit', None)
    if not user.is_authenticated() and first_visit != 'False':
        request.session['first_visit'] = 'False'
        return redirect('getstarted')
    lang = request.LANGUAGE_CODE
    popular = Website.objects.filter(lang__in=('multi', lang, )).order_by(
        '-popularity')[:5]
    offers = Offer.objects.exclude(number=0).order_by('?')[:5]
    new = Website.objects.filter(lang__in=('multi', lang, ))[:5]
    requests = Request.objects.filter(traded=False).order_by('?')
    # Get recentyly viewed sites
    recently_viewed = request.session.get('recently_viewed', list())
    if len(recently_viewed) > 0:
      recent_sites = Website.objects.filter(reduce(lambda x, y: x | y,
          [Q(pk=site_id) for site_id in recently_viewed]))
    else:
        recent_sites = None
    return render(request, 'market.html', {
        'popular': popular,
        'offers': offers,
        'new': new,
        'requests': requests,
        'recent_sites': recent_sites,
        })