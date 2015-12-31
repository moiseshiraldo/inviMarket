# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def partners(request, partner_id=None):
    """
    Display the partners list or the partner passed by argument.

    **Context**

    ``partners``
      An object array containing the partners.

    **Template:**

    :template:`inviMarket/partners.html`

    """
    user = request.user
    if partner_id is not None:
        partners = user.partners.filter(
          user_id=partner_id).select_related('user')
    else:
        partners = user.partners.all().select_related('user')
    paginator = Paginator(partners, 5)
    page = request.GET.get('page')
    try:
        partners = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        partners = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        partners = paginator.page(paginator.num_pages)
    return render(request, 'partners.html', {'partners': partners})