# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from inviMarket.forms import CategoryForm, TypeForm, OrderByForm
from inviMarket.models import Website
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.http import urlquote
import urllib
from django.utils.translation import ugettext as _
from inviMarket.decorators import cache_on_auth

@cache_on_auth(60 * 60)
def sites(request, site_name=None):
    """
    Display the forms for searching :model:`inviMarket.Website` and the results.

    **Context**

    ``category_form``
      An instace of the filter by category form.

    ``type_form``
      An instace of the filter by type form.

    ``order_form``
      An instace of the order by form.

    ``sites``
      The search results.

    **Template:**

    :template:`inviMarket/sites.html`

    """
    if site_name:
        # Requesting a specific site page
        site = get_object_or_404(Website, name=urllib.unquote(site_name))
        url = ('https://' + settings.DOMAIN +
               reverse('sites', kwargs={'site_name': urlquote(site.name) }))
        request.user.notification_set.filter(url=url).delete()
        lang = request.LANGUAGE_CODE
        try:
            # Get description in the user language
            description = site.description_set.get(lang=lang)
        except ObjectDoesNotExist:
            # Default None (English)
            description = None
        # Update recently viewed sites
        recent_sites = request.session.get('recent_sites', list())
        r_site = {'name': site.name, 'logo_url': site.logo.url, 'url': site.url}
        if r_site in recent_sites:
            recent_sites.remove(r_site)
            request.session['recent_sites'] = [r_site] + recent_sites
        elif len(recent_sites) > 4:
            request.session['recent_sites'] = [r_site] + recent_sites[:-1]
        else:
            request.session['recent_sites'] = [r_site] + recent_sites
        return render(request, 'site.html', {
            'site': site,
            'description': description,
            })
    message = query = None
    sites = Website.objects.all()
    if 'categories' in request.GET:
        category_form = CategoryForm(request.GET)
        if category_form.is_valid():
            categories = category_form.cleaned_data['categories']
            if len(categories) > 0:
                sites = sites.filter(reduce(lambda x, y: x | y,
                    [Q(category=c) for c in categories]))
    else:
        category_form = CategoryForm()
    if 'types' in request.GET:
        type_form = TypeForm(request.GET)
        if type_form.is_valid():
            types = type_form.cleaned_data['types']
            if len(types) > 0:
                sites = sites.filter(reduce(lambda x, y: x | y,
                    [Q(webType=t) for t in types]))
    else:
        type_form = TypeForm()
    if 'q' in request.GET and request.GET['q']:
        query = request.GET['q']
        if len(query) > 20:
            message = _("The query is too long:")
            query = query[:20] + "..."
        else:
            sites = sites.filter(name__icontains=query)
            message = _("Showing results for")
    if len(sites) == 0:
        message = _("No results matched the query")
        order_form = OrderByForm()
    else:
        if 'order' in request.GET:
            order_form = OrderByForm(request.GET)
            if order_form.is_valid():
                order = order_form.cleaned_data['order']
                sites.distinct()
                # Order by the selected option
                if order == 'PO':
                  sites = sites.order_by('-popularity')
                elif order == 'CA':
                  sites = sites.order_by('category')
                elif order == 'TY':
                  sites = sites.order_by('webType')
                elif order == 'RE':
                  sites = sites.order_by('-requests')
                elif order == 'OF':
                  sites = sites.order_by('-offers')
        else:
            order_form = OrderByForm()
            if not 'q' in request.GET:
                lang = request.LANGUAGE_CODE
                sites = Website.objects.filter(
                    lang__in=('multi', lang, )).order_by('-popularity')
        paginator = Paginator(sites, 4)
        page = request.GET.get('page')
        try:
            sites = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            sites = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver last page of results.
            sites = paginator.page(paginator.num_pages)
    # Get all queries to keep them in different pages
    queries = request.GET.copy()
    if 'page' in queries:
        del queries['page']
    return render(request, 'sites.html', {'category_form': category_form,
                                          'type_form': type_form,
                                          'order_form': order_form,
                                          'sites': sites,
                                          'message': message,
                                          'query': query,
                                          'queries': queries,
                                          })
