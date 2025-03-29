from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("contact-me/", views.contact_me, name="contact_me"),
    path("contact-forms/", views.contact_forms, name="contact_forms"),
    path("contact-form/<id>/", views.contact_form, name="contact_form"),
    path("delete-contact-form/<id>/", views.delete_contact_form, name="delete_contact_form"),
    path("contact-form/send-message/<id>/", views.send_message, name="send_message"),

]