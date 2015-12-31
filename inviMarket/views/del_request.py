# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _

from inviMarket.models import Request

@login_required
def del_request(request, site_id):
    """
    Delete the invite request passed by argument, related to
    :model:`inviMarket.Request`.

    **Context**

    ``message``
    Confirmation message.

    **Template:**

    :template:`inviMarket/message.html`

    """
    user = request.user
    req = get_object_or_404(Request, user=user, website=site_id)
    trades = req.trade_set.filter(accepted=False).prefetch_related(
        'requests', 'trades').iterator()
    # Lock the user to minimize concurrency problems
    if user.profile.lock_perm() and not req.traded:
        # Clear pending trades related to the request
        for trade in trades:
            trade.requests.clear()
            trade.offers.clear()
            trade.delete()
        req.delete()
        user.profile.unlock()
        message = _("The request has been deleted.")
    else:
        message = _("Some error has occurred. Reload and try again.")
    return render(request, 'message.html', {'message': message})