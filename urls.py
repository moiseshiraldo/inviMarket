from django.conf.urls import include, url
from django.contrib import admin
from inviMarket.language_url_prefix import custom_i18n_patterns

urlpatterns = [
    # Examples:
    # url(r'^$', 'inviProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += custom_i18n_patterns('',
    url(r'^', include('inviMarket.urls')),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^blog/', include('zinnia.urls', namespace='zinnia')),
)
