from django.shortcuts import render

from itbalgarche.models import AboutMe, Education, Certificate, Course, Achievement, ContactData


def index(request):

    latest_aboutme = AboutMe.objects.filter(is_active=True).latest('created_at')
    latest_education = Education.objects.filter(is_active=True).order_by('-created_at')
    latest_certificate = Certificate.objects.filter(is_active=True).order_by('-created_at')
    latest_course = Course.objects.filter(is_active=True).order_by('-created_at')
    latest_achievement = Achievement.objects.filter(is_active=True).order_by('-created_at')
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
