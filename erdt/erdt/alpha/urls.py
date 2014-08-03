from django.conf.urls import patterns, include, url
from erdt.alpha import views


urlpatterns = patterns('',
    url(r'^set-active-profile/(?P<profile_id>[0-9]+)$', views.set_active_profile, name='set-active-profile'),
)