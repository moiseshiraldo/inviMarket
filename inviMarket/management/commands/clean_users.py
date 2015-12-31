# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.utils import timezone

from inviMarket.models import User

class Command(BaseCommand):
    help = 'Calculate and update the rating of every user'

    def handle(self, *args, **options):
        inactive_users = User.objects.filter(is_active=False).select_related(
            'profile').iterator()
        now = timezone.now()
        for user in inactive_users:
            if user.profile.key_expires and user.profile.key_expires < now:
                user.profile.delete()
                user.delete()

        self.stdout.write(
          '{:%b %d %H:%M:%S} Users cleaning completed'.format(
            timezone.now()))