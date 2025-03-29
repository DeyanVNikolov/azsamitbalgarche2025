from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from itbalgarche.models import AboutMe, Education, Certificate, Course, Achievement, ContactData, ContactForm, \
    ContactFormMessage


def index(request):
    latest_aboutme = AboutMe.objects.filter(is_active=True).latest('created_at')
    latest_education = Education.objects.filter(is_active=True).order_by('-created_at')
    latest_certificate = Certificate.objects.filter(is_active=True).order_by('-created_at')
    latest_course = Course.objects.filter(is_active=True).order_by('-created_at')
    latest_achievement = Achievement.objects.filter(is_active=True).order_by('-date')
    latest_contact = ContactData.objects.filter(is_active=True).order_by('-created_at')

    context = {
        "aboutme": latest_aboutme,
        "education": latest_education,
        "certificate": latest_certificate,
        "course": latest_course,
        "achievement": latest_achievement,
        "contact": latest_contact,
    }

    return render(request, "home/index.html", context)


def contact_me(request):
    if request.method == "POST":
        name = request.POST.get("name") if not request.user.is_authenticated else request.user.username
        email = request.POST.get("email") if not request.user.is_authenticated else request.user.email
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        if not name or not email or not subject or not message:
            messages.error(request, "Please fill all fields")
            return redirect("/contact-me/")

        contact_form = ContactForm()
        contact_form.user = request.user if request.user.is_authenticated else None
        contact_form.name = name
        contact_form.subject = subject
        contact_form.email = email
        contact_form.save()

        contact_form_message = ContactFormMessage()
        contact_form_message.contact_form = contact_form
        contact_form_message.sender = request.user if request.user.is_authenticated else None
        contact_form_message.message = message
        contact_form_message.save()

        messages.success(request, "Your message has been sent successfully.")

        if request.user.is_authenticated:
            return redirect("/contact-form/{}".format(contact_form.id))

        return redirect("/contact-me/")

    return render(request, "home/contact_me.html")

@login_required
@staff_member_required
def contact_forms(request):
    contact_forms_data = ContactForm.objects.order_by('-created_at')

    context = {
        "contact_forms": contact_forms_data,
    }
    return render(request, "home/contact_forms.html", context)


def contact_form(request, id):


    if not request.user.is_authenticated:
        messages.error(request, "You are not authorized to access this page.")
        return redirect("/")

    contact_form_data = get_object_or_404(ContactForm, id=id, is_active=True)
    contact_form_messages = ContactFormMessage.objects.filter(contact_form=contact_form_data).order_by('-created_at').reverse()

    if not (request.user.is_superuser or (contact_form_data.user and contact_form_data.user == request.user)):
        messages.error(request, "You are not authorized to access this page.")
        return redirect("/")


    context = {
        "contact_form": contact_form_data,
        "contact_form_messages": contact_form_messages,
    }

    return render(request, "home/contact_form.html", context)


@login_required
@staff_member_required
def delete_contact_form(request, id):
    contact_form = get_object_or_404(ContactForm, id=id)
    contact_form.delete()
    messages.success(request, "Contact form deleted successfully.")

    return redirect("/contact-forms/")


def send_message(request, id):
    if request.method == "POST":
        contact_form = get_object_or_404(ContactForm, id=id)
        message = request.POST.get("message")

        if not message:
            messages.error(request, "Please fill all fields")
            return redirect("/contact-form/{}/".format(contact_form.id))

        contact_form_message = ContactFormMessage()
        contact_form_message.contact_form = contact_form
        contact_form_message.sender = request.user
        contact_form_message.message = message
        contact_form_message.save()

        messages.success(request, "Your message has been sent successfully.")

        return redirect("/contact-form/{}/".format(contact_form.id))