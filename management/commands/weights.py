# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from inviMarket.models import Offer
from django.db.models import F

class Command(BaseCommand):
    help = 'Calculate and update the weight of every referral offer'

    def handle(self, *args, **options):
        Offer.objects.filter(number=0, to_donate=1).update(
            weight=F('user__rating')+F('age')/100)

        self.stdout.write('Weights successfuly updated.')