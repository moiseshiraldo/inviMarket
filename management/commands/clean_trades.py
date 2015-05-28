# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone

from inviMarket.models import Trade

class Command(BaseCommand):
    help = 'Calculate and update the rating of every user'

    def handle(self, *args, **options):
        for trade in Trade.objects.filter(accepted=False).iterator():
            if trade.age() > settings.TRADE_EXPIRATION:
                if trade.receptor.profile.lock_perm():
                    trade.requests.clear()
                    trade.offers.clear()
                    trade.delete()
                    trade.receptor.notification_set.filter(code=10,
                        sender=trade.proposer).delete()
                    trade.receptor.profile.unlock()

        self.stdout.write(
          '{:%b %d %H:%M:%S} Expired trades cleaned'.format(
            timezone.now()))