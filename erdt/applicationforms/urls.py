from django.conf.urls import patterns, include, url
from applicationforms import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='applications-index'),
    url(r'^preregistration/$', views.display_prereg_form, name='display-preregistration'),
    url(r'^preregistration/submit/$', views.submit_prereg_form, name='submit-preregistration'),
    url(r'^preregistration/confirm/(?P<confirmation_token>.+)$', views.confirm_registration, name='confirm-preregistration'),
    url(r'^erdt-form/edit/$', views.edit_erdt_form, name='edit-erdt-form'),
    url(r'^erdt-form/submit/$', views.confirm_erdt_form, name='submit-erdt-form'),
    url(r'^recommendation-form/add/$', views.add_recommendation_form, name='add-recommendation-form'),
    url(r'^recommendation-form/send/$', views.send_recommendation_form, name='send-recommendation-form'),
    url(r'^recommendation-form/submit/$', views.confirm_recommendation_form, name='submit-recommendation-form'),
    url(r'^recommendation-form/edit/(?P<token_str>.+)$', views.edit_recommendation_form, name='edit-recommendation-form'),
    url(r'^recommendation-form/delete/$', views.delete_recommendation_form, name='delete-recommendation-form'),
)