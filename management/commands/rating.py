# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from inviMarket.models import User
from django.conf import settings
from django.utils import timezone

class Command(BaseCommand):
    help = 'Calculate and update the rating of every user'

    def handle(self, *args, **options):
      for user in User.objects.filter(is_active=True):
        proposed_trades = user.proposed_trade.filter(accepted=True)
        received_trades = user.received_trade.filter(accepted=True)
        trades = proposed_trades.filter(donation=False).count()
        trades += received_trades.filter(donation=False).count()
        donations = received_trades.filter(donation=True).count()
        sites = user.website_set.all().count()
        editions = user.edited_sites.all().count()
        user.profile.trades = trades
        user.profile.donations = donations
        months = (timezone.now() - user.profile.last_visit).months
        user.profile.rating = (settings.BASE_RATING + 5*donations + 3*trades
          + 2*sites + editions - 5*user.profile.warnings - months)
        user.profile.save()

      self.stdout.write('User ratings successfully updated')