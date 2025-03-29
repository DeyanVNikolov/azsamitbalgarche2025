from django import forms
from .models import AboutMe, Education, Certificate, Course, Achievement, ContactData


class AboutMeForm(forms.ModelForm):
    class Meta:
        model = AboutMe
        exclude = ['id', 'created_at', 'updated_at', 'is_active']


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ['id', 'created_at', 'updated_at', 'is_active']


class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        exclude = ['id', 'created_at', 'updated_at', 'is_active']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ['id', 'created_at', 'updated_at', 'is_active']


class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        exclude = ['id', 'created_at', 'updated_at', 'is_active']


class ContactDataForm(forms.ModelForm):
    class Meta:
        model = ContactData
        exclude = ['id', 'created_at', 'updated_at', 'is_active']
