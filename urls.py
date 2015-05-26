from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.utils.translation import ugettext as _
from django.contrib.sitemaps.views import sitemap

from inviMarket import views
from inviMarket.decorators import cache_on_auth

sitemaps = {
    'static': views.StaticViewSitemap,
    'sites': views.WebsiteSitemap,
}

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^legal/$',
        cache_on_auth(4*3600)(TemplateView.as_view(template_name="legal.html")),
        name='legal'),
    url(r'^faq/$',
        cache_on_auth(4*3600)(TemplateView.as_view(template_name="faq.html")),
        name='faq'),
    url(r'^getstarted/$',
        cache_on_auth(4*3600)(
            TemplateView.as_view(template_name="getstarted.html")),
        name='getstarted'),
    url(r'^glossary/$',
        cache_on_auth(4*3600)(
            TemplateView.as_view(template_name="glossary.html")),
        name='glossary'),
    url(r'^suggestions/$',
        cache_on_auth(4*3600)(
            TemplateView.as_view(template_name="suggestions.html")),
        name='suggestions'),
    url(r'^editing/$', TemplateView.as_view(template_name="editing.html"),
        name='editing'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register/confirm(?:/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<key>\w+))?/$',
        views.confirm, name='confirm'),
    url(r'^login(?:/(?P<next>\d+))?/$', views.user_login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'index'}, name='logout'),
    url(r'^profile/password/change/$', auth_views.password_change,
        {'template_name': 'password_change.html'}, name='password_change'),
    url(r'^profile/password/changed/$', auth_views.password_change_done,
        {'template_name': 'message.html',
        'extra_context': {'message': "Your password has been changed."}},
        name='password_change_done'),
    url(r'^profile/password/reset/$', auth_views.password_reset, {
        'template_name': 'password_reset.html',
        'post_reset_redirect': 'reset_sent',
        'email_template_name': 'email/password_reset.txt',
        'html_email_template_name': 'email/password_reset.html'
        }, name='password_reset'),
    url(r'^profile/password/reset/sent/$', auth_views.password_reset_done, {
        'template_name': 'message.html',
        'extra_context': {'message': "The password reset link have been sended "
          "to your email address"}
        }, name='reset_sent'),
    url(r'^profile/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/'
        '(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, {
          'template_name': 'reset_confirm.html',
          'post_reset_redirect': 'reset_done',
        }, name='reset_confirm'),
    url(r'^profile/password/reset/done/$', auth_views.password_reset_complete, {
        'template_name': 'reset_done.html',
        'extra_context': {'message': "Your password has been changed."}
        }, name='reset_done'),
    url(r'^profile(?:/(?P<user_id>\d+))?/$', views.profile, name='profile'),
    url(r'^sites/edition(?:/(?P<site_id>\d+))?/$', views.edition,
        name='edition'),
    url(r'^sites(?:/(?P<site_name>[0-9A-Za-z_\.%]+))?/$', views.sites,
        name='sites'),
    url(r'^sites/edition/submitted/$', views.MessageView.as_view(
        message=_("Your edition have been submitted and will be reviewed by "
                  "the admin.")
      ), name='edition_submitted'),
    url(r'^request/(?P<site_id>\d+)/$', views.request, name='request'),
    url(r'^request/delete/(?P<site_id>\d+)/$', views.del_request,
        name='del_request'),
    url(r'^offer/(?P<site_id>\d+)/$', views.offer, name='offer'),
    url(r'^offer/submitted/$', views.MessageView.as_view(
        message = _("Your offer has been succesfuly stored.")
        ), name='offer_submitted'),
    url(r'^offer/deleted/$', views.MessageView.as_view(
        message = _("The offer has been deleted.")
        ), name='offer_deleted'),
    url(r'^chain/(?P<site_id>\d+)/$', views.chain, name='chain'),
    url(r'^chain/created/$', views.MessageView.as_view(
        message = _("The referral chain has been created, you can get the link "
        "on your profile page.")
        ), name='chain_created'),
    url(r'^chain/join/(?P<cidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z_\-]+)/$',
        views.join_chain, name='join_chain'),
    url(r'^trading/$', views.trading, name='trading'),
    url(r'^propose/(?P<receptor_id>\d+)/$', views.propose, name='propose'),
    url(r'^propose/submitted/$', views.MessageView.as_view(
        message = _("Your trade proposal has been sended to the user.")
        ), name='proposal_submitted'),
    url(r'^profile/trades/$', views.trades, name='trades'),
    url(r'^profile/trade/(?P<trade_id>\d+)/$', views.trade, name='trade'),
    url(r'^profile/trade/accepted/$', views.MessageView.as_view(
        message = _("The trade proposal has been accepted.")
        ), name='trade_accepted'),
    url(r'^profile/trade/rejected/$', views.MessageView.as_view(
        message = _("The trade proposal has been rejected.")
        ), name='trade_rejected'),
    url(r'^profile/partners(?:/(?P<partner_id>\d+))?/$', views.partners,
        name='partners'),
    url(r'^profile/partners/add/(?P<partner_id>\d+)/$', views.add_partner,
        name='add_partner'),
    url(r'^profile/partners/delete/(?P<partner_id>\d+)/$', views.del_partner,
        name='del_partner'),
    url(r'^profile/config/$', views.config, name='config'),
    url(r'^profile/delete/$', views.del_profile, name='del_profile'),
    url(r'^profile/trade/complaint/(?P<trade_id>\d+)/$', views.complaint,
        name='complaint'),
    url(r'^profile/trade/complaint/submitted/$', views.MessageView.as_view(
        message = _("Your complaint has been submitted.")
        ), name='complaint_submitted'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap')
)