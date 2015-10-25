from django.conf.urls import patterns, include, url
from applicationforms import views


urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^preregistration/$', views.display_prereg_form, name='display-preregistration'),
    url(r'^preregistration/submit/$', views.submit_prereg_form, name='submit-preregistration'),
    url(r'^preregistration/confirm/(?P<confirmation_token>.+)$', views.confirm_registration, name='confirm-preregistration'),
    url(r'^preregistration/confirm/$', views.confirm_registration_dummy, name='confirm-preregistration-dummy'),
    url(r'^preregistration/erdt-form/edit/$', views.edit_erdt_form, name='edit-erdt-form'),
    url(r'^preregistration/erdt-form/submit/$', views.confirm_erdt_form, name='submit-erdt-form'),
)