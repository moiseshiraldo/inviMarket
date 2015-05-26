# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import ugettext as _

from inviMarket.forms import TradeForm, ShowDonationsForm

@login_required
def trading(request):
    """
    Display the trade searching form, look for other users matching up with
    the user requests/offers and show the search results.

    **Context**

    ``request_filter``
      An instance of the trade form containing the request choices.

    ``offer_filter``
      An instance of the trade form containing the offer choices.

    ``users``
      The search results.

    ``message``
      A variable string containing information about the search result.

    **Template:**

    :template:`inviMarket/trading.html`

    """

    message = request_filter = offer_filter = show_filter = None
    requests = offers = users = None
    user = request.user
    # Get the user requests and append the choices to a list
    user_requests = user.profile.get_requests()
    requests_len = len(user_requests)
    request_choices = list()
    requests_label = ""
    for r in user_requests:
        request_choices.append((r.website.pk, r.website))
    # Get the user offers and append the choices to a list
    user_offers = user.profile.get_offers()
    offers_len = len(user_offers)
    offer_choices = list()
    offers_label = ""
    for o in user_offers:
        offer_choices.append((o.website.pk, o.website))
    # Get the partners list and the reverse partners profile list
    partners_list = user.profile.partners.all()
    reverse_partners_list = user.partners.values_list('user_id', flat=True)
    if 'show' in request.GET:
        show_filter = ShowDonationsForm(request.GET)
        if show_filter.is_valid():
            show = show_filter.cleaned_data['show']
    elif requests_len:
        show_filter = ShowDonationsForm(request.GET)
    if 'request-sites' in request.GET:
        request_filter = TradeForm(request_choices, requests_label,
            request.GET, prefix='request')
        if request_filter.is_valid():
            # Search for users offering the selected requests
            requests = request_filter.cleaned_data['sites']
            users = User.objects.filter(offer__website__in=requests,
                offer__number__gt=0, offer__website__protected=False)
            # Protected (only partners)
            partners = partners_list.filter(offer__website__in=requests,
              offer__number__gt=0, offer__website__protected=True)
            # Exclude non-accepted partnership requests
            for partner in partners:
                if partner.id not in reverse_partners_list:
                    partners = partners.exclude(pk=partner.id)
            users = users | partners
            # Show only donatinos if selected
            if show == 'DON':
                users = users.filter(offer__website__in=requests,
                    offer__to_donate__gt=0)
    elif requests_len:
        request_filter = TradeForm(request_choices, requests_label,
            prefix='request')
    if 'offer-sites' in request.GET:
        offer_filter = TradeForm(offer_choices, offers_label,
            request.GET, prefix='offer')
        if offer_filter.is_valid():
            # Search for users requesting the selected offers
            offers = offer_filter.cleaned_data['sites']
            if users:
                users = users.filter(request__website__in=offers,
                  request__traded=False, request__website__protected=False)
            else:
                users = User.objects.filter(request__website__in=offers,
                  request__traded=False, request__website__protected=False)
            partners = partners_list.filter(request__website__in=offers,
                request__traded=False, request__website__protected=True)
            for partner in partners:
                if partner.id not in reverse_partners_list:
                    partners = partners.exclude(pk=partner.id)
            users = users | partners
    elif offers_len:
        offer_filter = TradeForm(offer_choices, offers_label, prefix='offer')
    # By default, search for users offering the requested sites
    if not requests and not offers:
        if requests_len:
            sites = list(dict(request_choices).keys())
            users = User.objects.filter(offer__website__in=sites,
                offer__number__gt=0, offer__website__protected=False)
            partners = partners_list.filter(offer__website__in=sites,
                offer__number__gt=0, offer__website__protected=True)
            for partner in partners:
                if partner.id not in reverse_partners_list:
                    partners = partners.exclude(pk=partner.id)
            users = users | partners
        elif offers_len:
            sites = list(dict(offer_choices).keys())
            users = User.objects.filter(request__website__in=sites,
                request__traded=False,
                request__website__protected=False)
            partners = partners_list.filter(request__website__in=sites,
                request__traded=False,
                request__website__protected=True)
            for partner in partners:
                if partner.id not in reverse_partners_list:
                    partners = partners.exclude(pk=partner.id)
            users = users | partners
        else:
            message = _("You have not made any request or offer yet.")
    if not message and users:
        # Eliminate duplicated users from the queryset and prepare pagination
        users = users.distinct()
        paginator = Paginator(users, 5)
        page = request.GET.get('page')
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            users = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver last page of results.
            users = paginator.page(paginator.num_pages)
    elif not message:
        message = _("No results")
    # Get all queries to keep them in different pages
    queries = request.GET.copy()
    if 'page' in queries:
        del queries['page']
    return render(request, 'trading.html', {
        'request_filter': request_filter,
        'offer_filter': offer_filter,
        'show_filter': show_filter,
        'users': users,
        'message': message,
        'queries': queries,
        })