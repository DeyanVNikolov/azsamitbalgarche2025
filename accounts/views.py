import uuid

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import CustomUser
from itbalgarche.models import (
    AboutMe, Education, Certificate, Course,
    Achievement, ContactData
)
from itbalgarche.forms import (
    AboutMeForm, EducationForm, CertificateForm,
    CourseForm, AchievementForm, ContactDataForm
)

MODEL_MAP = {
    'aboutme': (AboutMe, AboutMeForm),
    'education': (Education, EducationForm),
    'certificate': (Certificate, CertificateForm),
    'course': (Course, CourseForm),
    'achievement': (Achievement, AchievementForm),
    'contactdata': (ContactData, ContactDataForm),
}


def profile(request):
    return render(request, "accounts/profile.html")
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "auth/login.html")


def register_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            messages.error(request, "Passwords do not match.")
        elif CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use.")
        else:
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect("/")

    return render(request, "auth/register.html")


@login_required
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("/")

    return redirect("/")


@login_required
@staff_member_required
def cv_admin(request):
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to access this page.")
        return redirect("/")

    context = {
        'aboutme_list': AboutMe.objects.filter(is_active=True),
        'aboutme_history_list': AboutMe.objects.filter(is_active=False),
        'education_list': Education.objects.filter(is_active=True),
        'education_history_list': Education.objects.filter(is_active=False),
        'certificate_list': Certificate.objects.filter(is_active=True),
        'certificate_history_list': Certificate.objects.filter(is_active=False),
        'course_list': Course.objects.filter(is_active=True),
        'course_history_list': Course.objects.filter(is_active=False),
        'achievement_list': Achievement.objects.filter(is_active=True),
        'achievement_history_list': Achievement.objects.filter(is_active=False),
        'contactdata_list': ContactData.objects.filter(is_active=True),
        'contactdata_history_list': ContactData.objects.filter(is_active=False),
    }
    return render(request, "accounts/cv_admin.html", context)


@login_required
@staff_member_required
def cv_edit(request, model_name, record_id):
    if model_name not in MODEL_MAP:
        messages.error(request, "Invalid model specified.")
        return redirect("cv_admin")

    Model, FormClass = MODEL_MAP[model_name]
    instance = get_object_or_404(Model, id=record_id, is_active=True)

    if request.method == "POST":
        form = FormClass(request.POST)
        if form.is_valid():
            new_instance = Model.objects.create(**form.cleaned_data, is_active=True)
            Model.objects.filter(id=instance.id).update(is_active=False)
            messages.success(request, f"{model_name.capitalize()} record updated successfully.")
            return redirect("cv_admin")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        initial_data = {}
        for field in instance._meta.fields:
            if field.name not in ['id', 'created_at', 'updated_at', 'is_active']:
                initial_data[field.name] = getattr(instance, field.name)
        form = FormClass(initial=initial_data)

    context = {
        "form": form,
        "model_name": model_name,
        "record_id": record_id,
    }
    return render(request, "accounts/cv_edit.html", context)


@login_required
@staff_member_required
def cv_create(request, model_name):
    if model_name not in MODEL_MAP:
        messages.error(request, "Invalid model specified.")
        return redirect("cv_admin")
    Model, FormClass = MODEL_MAP[model_name]
    if request.method == "POST":
        form = FormClass(request.POST)
        if form.is_valid():
            Model.objects.create(**form.cleaned_data, is_active=True)
            messages.success(request, f"New {model_name.capitalize()} record created successfully.")
            return redirect("cv_admin")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = FormClass()
    context = {
        "form": form,
        "model_name": model_name,
    }
    return render(request, "accounts/cv_create.html", context)


@login_required
@staff_member_required
def cv_restore(request, model_name, record_id):
    if model_name not in MODEL_MAP:
        messages.error(request, "Invalid model specified.")
        return redirect("cv_admin")

    Model, _ = MODEL_MAP[model_name]

    instance = get_object_or_404(Model, id=record_id)

    if instance.is_active:
        instance.is_active = False
        instance.save()
    else:
        Model.objects.filter(id=instance.id).update(is_active=False)

    data = {}
    for field in instance._meta.fields:
        if field.name not in ['id', 'created_at', 'updated_at', 'is_active']:
            data[field.name] = getattr(instance, field.name)
    Model.objects.create(**data, is_active=True)

    messages.success(request, f"{model_name.capitalize()} record restored successfully.")
    return redirect("cv_admin")


@login_required
@staff_member_required
def cv_delete(request, model_name, record_id):
    if model_name not in MODEL_MAP:
        messages.error(request, "Invalid model specified.")
        return redirect("cv_admin")
    Model, _ = MODEL_MAP[model_name]
    instance = get_object_or_404(Model, id=record_id)
    instance.delete()
    messages.success(request, f"{model_name.capitalize()} record permanently deleted.")
    return redirect("cv_admin")


def cv_add_image(request):
    if request.method == "POST":
        img = request.FILES.get('image')
        if img:
            fs = FileSystemStorage(location='static/images/')
            filename = fs.save(f"{img.name.split('.')[0]}_{uuid.uuid4()}.{img.name.split('.')[-1]}", img)

            aboutme = AboutMe.objects.filter(is_active=True).latest('created_at')
            aboutme.image_name = filename
            aboutme.save()

            messages.success(request, "Image added successfully.")
            return redirect("cv_admin")
        else:
            messages.error(request, "No image provided.")
            return redirect("cv_admin")

    return render(request, "accounts/cv_upload_image.html")
