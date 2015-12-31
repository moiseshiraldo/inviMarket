# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import ugettext as _

from inviMarket.forms import TradeFilter
from inviMarket.models import Trade

@login_required
def trades(request):
    """
    Display the trades related to the current user.

    **Context**

    ``trade_filter``
      An instance of the trade filter form.

    ``trades``
      The search results.

    ``message``
      A string variable containing search information.

    **Template:**

    :template:`inviMarket/yourtrades.html`

    """
    user = request.user
    message = None
    # By default, display all trades related to the user
    trades = Trade.objects.filter(Q(proposer=user) | Q(receptor=user))
    if 'status' in request.GET:
        trade_filter = TradeFilter(request.GET)
        if trade_filter.is_valid() and trades:
            # Filter trades by the selected status
            status = trade_filter.cleaned_data['status']
            if len(status)>0:
                if 'RE' not in status:
                    trades = trades.exclude(receptor=user, accepted=False)
                if 'SE' not in status:
                    trades = trades.exclude(proposer=user, accepted=False)
                if 'AC' not in status:
                    trades = trades.exclude(accepted=True)
    else:
        trade_filter = TradeFilter()
    if trades:
        paginator = Paginator(trades, 5)
        page = request.GET.get('page')
        try:
            trades = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            trades = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver last page of results.
            trades = paginator.page(paginator.num_pages)
    else:
        message = _("You don't have any trade.")
    # Get all queries to keep them in different pages
    queries = request.GET.copy()
    if 'page' in queries:
        del queries['page']
    return render(request, 'trades.html', {
        'trade_filter': trade_filter,
        'trades': trades,
        'message': message,
        'queries': queries,
        })