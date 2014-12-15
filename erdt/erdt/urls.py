from django.conf.urls import patterns, include, url
from erdt.alpha.admin import admin_site
from erdt.alpha import views as alpha_views
from django.conf import settings
import smart_selects, django_select2

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'erdt.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Set media url
    # Set our homepage to the admin_site
    url(r'^', include(admin_site.urls)),
    url(r'^', include('erdt.alpha.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^select2/', include('django_select2.urls')),
    #url(r'^community/', include('django_website.aggregator.urls', namespace='community')),
)
