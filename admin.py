from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from inviMarket.models import *

# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class NotificationInline(admin.TabularInline):
    model = Notification
    fk_name = 'user'
    verbose_name_plural = 'Notifications'

class RequestInline(admin.TabularInline):
    model = Request
    verbose_name_plural = 'Requests'

class OfferInline(admin.TabularInline):
    model = Offer
    verbose_name_plural = 'Offers'

class DescriptionInline(admin.TabularInline):
    model = Description
    verbose_name_plural = 'Descriptions'

class LinkInline(admin.TabularInline):
    model = Link
    verbose_name_plural = 'Links'

class UserAdmin(UserAdmin):
    inlines = (ProfileInline, NotificationInline, RequestInline, OfferInline )

class WebsiteAdmin(admin.ModelAdmin):
    inlines = (DescriptionInline,)

class ChainAdmin(admin.ModelAdmin):
    inlines = (LinkInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(Chain, ChainAdmin)
admin.site.register(SiteEdition)
admin.site.register(Trade)
admin.site.register(Complaint)
