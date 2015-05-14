# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from inviMarket.models import Website
from django.db.models import Count, Sum, Max, F

class Command(BaseCommand):
    help = 'Calculate and update the popularity of every site'

    def handle(self, *args, **options):
        ref_sites = Website.objects.filter(active=True,
            category='RE').annotate(n_links=Count('offer'))
        links = ref_sites.aggregate(total=Max('n_links'))
        sites = Website.objects.filter(active=True).exclude(
            category='RE').annotate(
                              n_offers=Sum('offer__number'),
                              n_requests=Count('request'),
                              )
        total = sites.aggregate(
                        offers=Max('n_offers'),
                        requests=Max('n_requests'),
                        )
        for site in ref_sites:
            site.offers = site.n_links
            site.popularity = site.n_links*100/links['total']
            site.save()
        for site in sites:
            site.offers = site.n_offers
            site.requests = site.n_requests
            site.popularity = (site.n_offers*100/(2*total['offers'])
                               + site.n_requests*100/(2*total['requests']))
            site.save()

        self.stdout.write('Sites popularities successfully updated')