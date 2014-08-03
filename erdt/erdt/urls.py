from django.conf.urls import patterns, include, url
from erdt.alpha.admin import admin_site
from erdt.alpha import views as alpha_views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'erdt.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Set our homepage to the admin_site 
    url(r'^', include(admin_site.urls)),
    url(r'^', include('erdt.alpha.urls')),
    #url(r'^community/', include('django_website.aggregator.urls', namespace='community')),
)
