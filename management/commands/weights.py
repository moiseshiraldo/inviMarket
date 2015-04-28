# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from inviMarket.models import Offer
import datetime

class Command(BaseCommand):
    help = 'Calculate and update the weight of every referral offer'

    def handle(self, *args, **options):
      for offer in Offer.objects.filter(number=0, to_donate=1):
        age = (datetime.date.today() - offer.date).days
        rating = offer.user.rating
        offer.weight = rating + age/100
        offer.save()

      self.stdout.write('Weights successfuly updated.')