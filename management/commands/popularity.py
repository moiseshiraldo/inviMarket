# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.db.models import Count, Sum, Max

from inviMarket.models import Website
from inviMarket.analytics import get_analytics

class Command(BaseCommand):
    help = 'Calculate and update the popularity of every site'

    def handle(self, *args, **options):
        ref_sites = Website.objects.filter(active=True,
            category='RE').annotate(n_links=Count('offer'))
        links = ref_sites.aggregate(total=Max('n_links'))
        sites = Website.objects.filter(active=True).exclude(
            category='RE').annotate(n_offers=Sum('offer__number'))
        page_views = dict(get_analytics(metric_id='pageviews',
            dimension_id='pageTitle').get('rows'))
        for key in page_views.keys():
            if not 'InviMarket: ' in key:
                del page_views[key]
        if page_views:
            max_views = max(map(int, page_views.values()))
        else:
            max_views = 1
        for site in ref_sites:
            site.offers = site.n_links
            site_views = int(page_views.get('InviMarket: ' + site.name, 0))
            site.popularity = (site.n_links*100/2*links['total']
                               + site_views*100/2*max_views)
            site.save()
        for site in sites:
            site.requests = site.request_set.filter(traded=False).count()
            site.offers = site.n_offers
            site_views = int(page_views.get('InviMarket: ' + site.name, 0))
        total = sites.aggregate(
                        offers=Max('n_offers'),
                        requests=Max('requests'),
                        )
        for site in sites:
            site.popularity = (site.n_offers*100/(3*total['offers'])
                               + site.requests*100/(3*total['requests'])
                               + site_views*100/3*max_views)
            site.save()

        self.stdout.write('Sites popularities successfully updated')