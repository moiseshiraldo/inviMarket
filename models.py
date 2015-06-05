# -*- encoding: utf-8 -*-
from django.db import models
from django.db import transaction
from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

from django.utils import timezone
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

import os
import datetime

def avatar_file_name(instance, filename):
    img = 'avtr' + str(instance.user.id) + '.png'
    path = os.path.join(settings.MEDIA_ROOT, img)
    if os.path.exists(path):
        os.remove(path)
    return img

def validate_image(img_object):
    size = img_object.file.size
    if size > 25*1024:
        raise ValidationError(_("Max file size is 25KB"))

LANG = (
    ('es', _('Spanish')),
    ('en', _('English')),
)
SITE_LANG = (
    ('es', _('Spanish')),
    ('en', _('English')),
    ('multi', _('Multi-language')),
)

class Profile(models.Model):
    """
    Stores the user profile, related to :model:`auth.User`.

    """
    user = models.OneToOneField(User)
    partners = models.ManyToManyField(User, related_name='partners', blank=True)
    avatar = models.ImageField(upload_to=avatar_file_name,
                               validators=[validate_image],
                               null=True, blank=True)
    rating = models.PositiveSmallIntegerField(default=settings.BASE_RATING)
    trades = models.PositiveIntegerField(default=0)
    donations = models.PositiveIntegerField(default=0)
    lang = models.CharField(max_length=5, choices=LANG, blank=True)
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField(null=True, blank=True)
    last_visit = models.DateTimeField(blank=True, null=True)
    notify = models.BooleanField(default=True)
    locked = models.BooleanField(default=False)

    def get_rating(self):
        if self.rating == 0:
            return mark_safe('<span class="low">Banned</span>')
        elif self.rating < 10:
            return mark_safe('<span class="low">D</span>')
        elif self.rating < 25:
            return mark_safe('<span class="low">D+</span>')
        elif self.rating < 35:
            return mark_safe('<span class="medium">C</span>')
        elif self.rating < 50:
            return mark_safe('<span class="medium">C+</span>')
        elif self.rating < 65:
            return mark_safe('<span class="medium">B</span>')
        elif self.rating < 80:
            return mark_safe('<span class="high">B+</span>')
        elif self.rating < 95:
            return mark_safe('<span class="high">A</span>')
        else:
            return mark_safe('<span class="high">A+</span>')
    def count_notifications(self):
        return self.user.notification_set.count()
    def get_requests(self):
        return self.user.request_set.filter(traded=False)
    def get_offers(self):
        return self.user.offer_set.filter(number__gt=0)
    def get_reflinks(self):
        return self.user.offer_set.filter(number=0, to_donate=1)
    @transaction.atomic
    def lock_perm(self):
        profile = Profile.objects.select_for_update().get(id=self.id)
        if profile.locked == False:
            profile.locked = True
            profile.save()
            return True
        return False
    def unlock(self):
        self.locked = False
        self.save()
    def __unicode__(self):
        return "%s's profile" % self.user

class Notification(models.Model):
    """
    Stores the user's notifications, related to :model:`auth.User`.

    """
    user = models.ForeignKey(User)
    sender = models.ForeignKey(User, null=True, blank=True,
                               related_name='sent_notification')
    code = models.PositiveSmallIntegerField(default=0)
    url = models.URLField()
    date = models.DateField(auto_now=True)
    MESSAGE = {
        10: _('Trade proposal'),
        20: _('Partnership request'),
        30: _('Proposal accepted'),
        40: _('Approved edition'),
        50: _('Received warning'),
    }

    def get_message(self):
        return self.MESSAGE[self.code]
    def __unicode__(self):
        return "Notification for %s" % self.user


class Website(models.Model):
    """
    Stores a website and its basic information.

    """
    name = models.CharField(max_length=20, unique=True, db_index=True)
    author = models.ForeignKey(User, blank=True, null=True)
    url = models.URLField()
    logo = models.ImageField(upload_to='sites/', null=True, blank=True)
    refvalidator = models.CharField(max_length=200, blank=True)
    email_domain = models.CharField(max_length=200, blank=True, db_index=True)
    lang = models.CharField(max_length=5, choices=SITE_LANG, blank=True)
    WTYPE = (
        ('APP', _('Application')),
        ('CS', _('Cloud Service')),
        ('CO', _('Community')),
        ('DD', _('Direct Download')),
        ('PTC', _('Paid-To-Click')),
        ('P2P', _('Peer to peer')),
        ('SN', _('Social network')),
        ('ST', _('Streaming')),
        ('TR', _('Tracker')),
    )
    webType = models.CharField(max_length=3, choices=WTYPE)
    CAT = (
        ('CUL', _('Culture')),
        ('EC', _('E-commerce')),
        ('GEN', _('Generic')),
        ('MMD', _('Multimedia')),
        ('RE', _('Referral')),
        ('TEL', _('Telecommunications')),
    )
    category = models.CharField(max_length=3, choices=CAT)
    popularity = models.PositiveSmallIntegerField(default=0)
    requests = models.PositiveIntegerField(default=0)
    offers = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    protected = models.BooleanField(default=False)

    def get_category(self):
        return dict(self.CAT)[self.category]
    def get_type(self):
        return dict(self.WTYPE)[self.webType]
    def get_lang(self):
        return dict(SITE_LANG)[self.lang]
    def __unicode__(self):
        return self.name

class Description(models.Model):
    """
    Stores a website description.

    """
    site = models.ForeignKey(Website)
    text = models.TextField()
    source = models.URLField(blank=True)
    lang = models.CharField(max_length=5, choices=LANG, blank=True)

    def __unicode__(self):
        return "Description for %s" % self.site

class SiteEdition(models.Model):
    """
    Stores a website edition proposal.

    """
    user = models.ForeignKey(User, related_name="editions")
    site = models.ForeignKey(Website, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=20)
    url = models.URLField()
    refvalidator = models.CharField(max_length=200, blank=True)
    email_domain = models.CharField(max_length=200, blank=True)
    description = models.TextField(max_length=5000, blank=True)
    source = models.URLField(blank=True, null=True)
    lang = models.CharField(max_length=5, choices=SITE_LANG)
    webType = models.CharField(max_length=3, choices=Website.WTYPE)
    category = models.CharField(max_length=3, choices=Website.CAT)
    active = models.BooleanField(default=True)
    comments = models.TextField(max_length=400, blank=True)
    approved = models.BooleanField(default=False)

    def __unicode__(self):
        return "Edition proposal for %s" % self.name

class Request(models.Model):
    """
    Stores an invite request made by an user, related to :model:`auth.User` and
    :model:`inviMarket:Website`.

    """
    user = models.ForeignKey(User)
    website = models.ForeignKey(Website)
    date = models.DateField(auto_now_add=True)
    traded = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s's request to %s" % (self.user, self.website)


class Offer(models.Model):
    """
    Stores an invite offer made by an user, related to :model:`auth.User` and
    :model:`inviMarket:Website`.

    """
    user = models.ForeignKey(User)
    website = models.ForeignKey(Website)
    date = models.DateField(auto_now_add=True)
    number = models.PositiveSmallIntegerField(default=0)
    to_donate = models.PositiveSmallIntegerField(default=0)
    referral = models.URLField(blank=True)
    weight = models.PositiveSmallIntegerField(default=0)

    def age(self):
        return (datetime.date.today() - self.date).days
    def __unicode__(self):
        return "%s's offer to %s" % (self.user, self.website)

class Chain (models.Model):
    """
    Stores a referral chain initiated by an user, related to :model:`auth.User`
    and :model:`inviMarket:Website`.

    """
    owner = models.ForeignKey(User)
    website = models.ForeignKey(Website)
    url_hash = models.CharField(max_length=40)
    password = models.CharField(max_length=20, blank=True)
    jumps = models.PositiveSmallIntegerField(default=1)

    def get_url(self):
        cidb64 = urlsafe_base64_encode(force_bytes(self.id))
        return 'http://' + settings.DOMAIN + reverse('join_chain',
            kwargs={'cidb64': cidb64, 'token': self.url_hash})
    def get_active_link(self):
        return self.link_set.get(active=True)
    def get_last_link(self):
        return self.link_set.get(last_link=True)
    @transaction.atomic
    def add_link(self, link):
        last = self.get_last_link()
        last.next_link = link
        last.last_link = False
        last.save()
        link.last_link = True
        link.save()
        link.source_link.counter -= 1
        if link.source_link.counter == 0:
            link.source_link.active = False
            link.source_link.next_link.active = True
            link.source_link.next_link.save()
        link.source_link.save()

    def __unicode__(self):
        return "%s's referral chain to %s" % (self.owner, self.website)

class Link(models.Model):
    """
    Stores a referral chain's link, related to :model:`inviMarket.Offer`

    """
    user = models.ForeignKey(User)
    chain = models.ForeignKey(Chain)
    source_link = models.ForeignKey('Link', related_name='children_links',
                                    null=True, blank=True)
    next_link = models.ForeignKey('Link', related_name='previous_link',
                                  null=True, blank=True)
    date = models.DateTimeField(auto_now=True)
    counter = models.PositiveSmallIntegerField()
    active = models.BooleanField(default=False)
    last_link = models.BooleanField(default=False)

class Trade(models.Model):
    """
    Stores an invites trade proposed by an user, related to :model:`auth.User`,
    :model:`inviMarket.Request` and :model:`inviMarket.Offer`.

    """
    proposer = models.ForeignKey(User, related_name='proposed_trades')
    receptor = models.ForeignKey(User, related_name='received_trades')
    requests = models.ManyToManyField(Request)
    offers = models.ManyToManyField(Offer)
    donation = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)
    comments = models.TextField(max_length=400, blank=True)
    accepted = models.BooleanField(default=False)

    def age(self):
        return (timezone.now() - self.date).days
    def get_proposer_requests(self):
        return self.requests.filter(user=self.proposer)
    def get_receptor_requests(self):
        return self.requests.filter(user=self.receptor)
    def get_proposer_offers(self):
        return self.offers.filter(user=self.proposer)
    def get_receptor_offers(self):
        return self.offers.filter(user=self.receptor)
    def __unicode__(self):
        return "%s's trade proposal to %s" % (self.proposer, self.receptor)

class Complaint(models.Model):
    """
    Stores a trade complaint, related to :model:`auth.User` and
    :model:`inviMarket.Trade`.

    """
    user = models.ForeignKey(User)
    receptor = models.ForeignKey(User, related_name='received_complaints')
    trade = models.ForeignKey(Trade)
    auto = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    comments = models.TextField(max_length=400, blank=True)

class Email(models.Model):
    """
    Stores the email related to a :model:`inviMarket.Complain`

    """
    complaint = models.ForeignKey(Complaint)
    from_address = models.CharField(max_length=320)
    subject = models.TextField()
    text = models.TextField()





