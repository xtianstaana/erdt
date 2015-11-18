from django.conf.urls import patterns, include, url
from applicationforms import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='applications-index'),
    # Pre-registration
    url(r'^preregistration/$', views.display_prereg_form, name='display-preregistration'),
    url(r'^preregistration/submit/$', views.submit_prereg_form, name='submit-preregistration'),
    url(r'^preregistration/confirm/(?P<confirmation_token>.+)$', views.confirm_registration, name='confirm-preregistration'),
    
    # ERDT Application Form
    url(r'^erdt-form/edit/$', views.edit_erdt_form, name='edit-erdt-form'),
    url(r'^erdt-form/submit/$', views.confirm_erdt_form, name='submit-erdt-form'),

    # UP Graduate Application Form
    url(r'^up-grad-form/edit/$', views.edit_upgrad_form, name='edit-upgrad-form'),
    url(r'^up-grad-form/submit/$', views.confirm_upgrad_form, name='submit-upgrad-form'),

    # UPD - ERDT Application Form
    url(r'^upd-erdt-form/edit/$', views.edit_upderdt_form, name='edit-upderdt-form'),
    url(r'^upd-erdt-form/submit/$', views.confirm_upderdt_form, name='submit-upderdt-form'),
    

    # Recommendation Form
    url(r'^recommendation-form/add/$', views.add_recommendation_form, name='add-recommendation-form'),
    url(r'^recommendation-form/send/$', views.send_recommendation_form, name='send-recommendation-form'),
    url(r'^recommendation-form/submit/$', views.confirm_recommendation_form, name='submit-recommendation-form'),
    url(r'^recommendation-form/edit/(?P<token_str>.+)$', views.edit_recommendation_form, name='edit-recommendation-form'),
    url(r'^recommendation-form/delete/$', views.delete_recommendation_form, name='delete-recommendation-form'),
)