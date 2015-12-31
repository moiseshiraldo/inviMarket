# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django import forms
from django.utils.translation import ugettext as _

from inviMarket.forms import EditionForm
from inviMarket.models import Website

@login_required
def edition(request, site_id=None):
    """
    Display the site edition form and store the proposal in the database.
    Related to :model:`inviMarket.SiteEdition`.

    **Context**

    ``edit_form``
      An instance of the site edition form.

    **Template:**

    :template:`inviMarket/edition.html`

    """
    user = request.user
    error = None
    if user.editions.filter(approved=False).exists():
        error = _("You have another edition pending for review. We will do it"
                  "as soon as possible, thank you for your patience.")
    elif request.method == 'POST':
        edit_form = EditionForm(request.POST)
        if edit_form.is_valid():
            edition = edit_form.save(commit=False)
            edition.user = user
            if site_id:
                site = get_object_or_404(Website, pk=site_id)
                edition.site = site
            edition.save()
            return redirect('edition_submitted')
    else:
        if site_id:
            site = get_object_or_404(Website, pk=site_id)
            try:
                description = site.description_set.get(
                    lang=request.LANGUAGE_CODE).text
            except ObjectDoesNotExist:
                description = None
            edit_form = EditionForm(initial={'name': site.name,
                                             'url': site.url,
                                             'refvalidator': site.refvalidator,
                                             'email_domain': site.email_domain,
                                             'description': description,
                                             'webType': site.webType,
                                             'lang': request.LANGUAGE_CODE,
                                             'category': site.category,
                                             })
            if site.category == 'RE':
                edit_form.fields['email_domain'].widget = forms.HiddenInput()
            else:
                edit_form.fields['refvalidator'].widget = forms.HiddenInput()
        else:
            edit_form = EditionForm()
    return render(request, 'edition.html', {
        'edit_form': edit_form,
        'site_id': site_id,
        'error': error,
        })