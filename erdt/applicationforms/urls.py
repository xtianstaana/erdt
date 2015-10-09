from django.conf.urls import patterns, include, url
from applicationforms import views


urlpatterns = patterns('',
    url(r'^preregistration/$', views.display_prereg_form),
    url(r'^preregistration/submit/$', views.submit_prereg_form, name='submit-preregistration'),
    url(r'^preregistration/confirm/(?P<confirmation_token>.+)$', views.confirm_registration, name='confirm-preregistration'),
    #url(r'^set-active-profile/(?P<profile_id>[0-9]+)$', views.set_active_profile, name='set-active-profile'),
    #url(r'^create_university_report_pdf/(?P<university_report_id>[0-9]+)$', reporting_views.create_university_report_pdf, name='create_university_report_pdf'),
    #url(r'^create_individual_report_pdf/(?P<individual_report_id>[0-9]+)$', reporting_views.create_individual_report_pdf, name='create_individual_report_pdf'),
    #url(r'^faculty_advisees/(?P<faculty_id>[0-9]+)$', reporting_views.create_list_advisees, name='create_list_advisees'),
)