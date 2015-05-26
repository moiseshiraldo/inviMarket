# -*- coding: utf-8 -*-
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.conf import settings

from inviMarket.models import SiteEdition, Complaint, Notification

@receiver(pre_save, sender=SiteEdition)
def approved_edition(sender, instance, **kwargs):
    try:
        old_edition = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass # Object is new
    else:
        # Field has changed
        if old_edition.approved == False and instance.approved == True:
            url = ('https://' + settings.DOMAIN +
               reverse('sites', kwargs={'site_name': instance.site.name }))
            notification = Notification(user=instance.user, code=40, url=url)
            notification.save()
            text = render_to_string('email/edition.txt', {
                                    'name': instance.user.first_name,
                                    'site_name': instance.site.name,
                                    'domain': settings.DOMAIN,
                                    'LANGUAGE_CODE': instance.user.profile.lang,
                                    })
            html = render_to_string('email/edition.html', {
                                    'name': instance.user.first_name,
                                    'site_name': instance.site.name,
                                    'domain': settings.DOMAIN,
                                    'LANGUAGE_CODE': instance.user.profile.lang,
                                    })
            subject = "Approved edition"
            send_mail(subject, text,
                      "inviMarket <no-reply@inviMarket.com>",
                      [instance.user.email],
                      html_message=html,
                      fail_silently=False)

@receiver(pre_save, sender=Complaint)
def accepted_complaint(sender, instance, **kwargs):
    try:
        old_complaint = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass # Object is new
    else:
        # Field has changed
        if old_complaint.accepted == False and instance.accepted == True:
            url = ('https://' + settings.DOMAIN +
               reverse('trade', kwargs={'trade_id': instance.trade.id }))
            notification = Notification(user=instance.receptor, code=50, url=url)
            notification.save()
            text = render_to_string('email/warning.txt', {
                                    'name': instance.receptor.first_name,
                                    'trade_id': instance.trade_id,
                                    'domain': settings.DOMAIN,
                                    'LANGUAGE_CODE': instance.receptor.profile.lang,
                                    })
            html = render_to_string('email/warning.html', {
                                    'name': instance.receptor.first_name,
                                    'trade_id': instance.trade_id,
                                    'domain': settings.DOMAIN,
                                    'LANGUAGE_CODE': instance.receptor.profile.lang,
                                    })
            subject = "Received warning"
            send_mail(subject, text,
                      "inviMarket <no-reply@inviMarket.com>",
                      [instance.receptor.email],
                      html_message=html,
                      fail_silently=False)