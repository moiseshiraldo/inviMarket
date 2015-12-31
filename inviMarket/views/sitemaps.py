# -*- coding: utf-8 -*-
from django.contrib import sitemaps
from django.core.urlresolvers import reverse
from django.utils.http import urlquote

from inviMarket.models import Website

class StaticViewSitemap(sitemaps.Sitemap):
    changefreq = 'daily'

    def items(self):
        return ['index', 'legal', 'faq', 'getstarted', 'glossary',
                'suggestions', 'editing', 'register', 'login', 'sites']

    def location(self, item):
        return reverse(item)

class WebsiteSitemap(sitemaps.Sitemap):
    changefreq = "daily"

    def items(self):
        return Website.objects.all()

    def location(self, item):
        return reverse('sites', kwargs={'site_name': urlquote(item.name)})

