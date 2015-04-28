# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from inviMarket.models import Website
from django.db.models import Count, Sum, F

class Command(BaseCommand):
    help = 'Calculate and update the popularity of every site'

    def handle(self, *args, **options):
        ref_sites = Website.objects.filter(active=True,
            category='RE').annotate(
                              links=Count('offer')
                              ).aggregate(
                                  total_links=Sum('links')
                                  )
        sites = Website.objects.filter(active=True).exclude(
            category='RE').annotate(
                              n_offers=Sum('offer__number'),
                              n_requests=Count('request'),
                            ).aggregate(
                                total_offers=Sum('n_offers'),
                                total_requests=Sum('n_requests'),
                                )
        ref_sites.update(
            links=F('n_links'),
            popularity=F('n_links')/F('total_links'),
        )
        sites.update(
            offers=F('n_offers'),
            requests=F('n_requests'),
            popularity=(F('n_offers')/2*F('total_offers') +
                        F('n_requests')/2*F('total_requests')),
        )

        self.stdout.write('Sites popularities successfully updated')