# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings

from inviMarket.models import User

import mailbox
import datetime, time

class Command(BaseCommand):
    help = 'Calculate and update the rating of every user'

    def handle(self, *args, **options):
        users = User.objects.filter(is_active=True).iterator()
        keep_time = (timezone.now() -
            datetime.timedelta(settings.COMPLAINT_DEADLINE))
        for user in users:
            if not user.complaint_set.filter(accepted=False).exists():
                dirname = settings.MAILDIR + user.username
                mbox = mailbox.Maildir(dirname, factory=None)
                for key, message in mbox.iteritems():
                    if message.get_date() < time.mktime(keep_time.timetuple()):
                        mbox.remove(key)

        self.stdout.write('Emails cleaning completed')