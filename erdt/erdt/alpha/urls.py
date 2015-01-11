from django.conf.urls import patterns, include, url
from erdt.alpha import views
from reporting import views as reporting_views


urlpatterns = patterns('',
    url(r'^set-active-profile/(?P<profile_id>[0-9]+)$', views.set_active_profile, name='set-active-profile'),
    url(r'^create_university_report_pdf/(?P<university_report_id>[0-9]+)$', reporting_views.create_university_report_pdf, name='create_university_report_pdf'),
    url(r'^create_individual_report_pdf/(?P<individual_report_id>[0-9]+)$', reporting_views.create_individual_report_pdf, name='create_individual_report_pdf'),
)