# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from inviMarket.models import User
from django.utils import timezone
from django.conf import settings
import mailbox

class Command(BaseCommand):
    help = 'Calculate and update the rating of every user'

    def handle(self, *args, **options):
        users = User.objects.filter(is_active=True).iterator()
        keep_time = (timezone.now() - settings.COMPLAINT_DEADLINE).seconds
        for user in users:
            if not user.complaint_set.filter(accepted=False).exists():
                dirname = settings.MAILDIR + user.username
                mbox = mailbox.Maildir(dirname, factory=None, create=None)
                for message in mbox:
                    if message.get_date() < keep_time:
                        del message

        self.stdout.write('Users cleaning completed')