# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone

from inviMarket.models import User

class Command(BaseCommand):
    help = 'Calculate and update the rating of every user'

    def handle(self, *args, **options):
        for user in User.objects.filter(is_active=True):
            proposed_trades = user.proposed_trades.filter(accepted=True)
            received_trades = user.received_trades.filter(accepted=True)
            trades = proposed_trades.filter(donation=False).count()
            trades += received_trades.filter(donation=False).count()
            donations = received_trades.filter(donation=True).count()
            sites = user.website_set.all().count()
            editions = user.editions.filter(approved=True).count()
            warnings = user.received_complaints.filter(accepted=True).count()
            if warnings >= 3:
                user.is_active = False
                user.profile.rating = 0
                user.profile.key_expires = None
                user.save()
                user.profile.save()
            else:
                user.profile.trades = trades
                user.profile.donations = donations
                days = (timezone.now() - user.profile.last_visit).days
                rating = (
                    settings.BASE_RATING
                    + 4*donations
                    + 2*trades
                    + 2*sites
                    + editions
                    - 5*warnings
                    - days/7)
                if rating > 100:
                    user.profile.rating = 100
                elif rating < 0:
                    user.profile.rating = 0
                else:
                    user.profile.rating = rating
                user.profile.save()

        self.stdout.write(
          '{:%b %d %H:%M:%S} User ratings successfully updated'.format(
            timezone.now()))