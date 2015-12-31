# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.db.models import F
from django.utils import timezone

from inviMarket.models import Offer

class Command(BaseCommand):
    help = 'Calculate and update the weight of every referral offer'

    def handle(self, *args, **options):
        offers = Offer.objects.filter(number=0, to_donate=1).annotate(
            rating=F('user__profile__rating')).iterator()
        for offer in offers:
            offer.weight = offer.rating + offer.age()/100
            offer.save()

        self.stdout.write(
          '{:%b %d %H:%M:%S} Link weights successfuly updated'.format(
              timezone.now()))