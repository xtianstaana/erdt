from django.conf.urls import patterns, include, url
from erdt.alpha import views


urlpatterns = patterns('',
    url(r'^set-active-profile/(?P<profile_id>[0-9]+)$', views.set_active_profile, name='set-active-profile'),
    url(r'^faculty_advisees/(?P<faculty_id>[0-9]+)$', views.create_list_advisees, name='create_list_advisees'),
    url(r'^faculty_equipment/(?P<faculty_id>[0-9]+)$', views.create_list_equipment, name='create_list_equipment'),
)