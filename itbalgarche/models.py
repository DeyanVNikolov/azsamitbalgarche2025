import uuid

from django.db import models

from azsamitbalgarche import settings


class AboutMe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image_name = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField()
    name = models.CharField(max_length=255)
    underline = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{} - {}".format(self.id, self.is_active)

    class Meta:
        verbose_name = "About Me"
        verbose_name_plural = "About Me"
        ordering = ['-created_at']


class Education(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school_name = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    start_date = models.CharField(max_length=255)
    end_date = models.CharField(max_length=255)
    graduated = models.BooleanField(default=False)
    description = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{} - {}".format(self.id, self.is_active)

    class Meta:
        verbose_name = "Education"
        verbose_name_plural = "Education"
        ordering = ['-created_at']


class Certificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    issued_by = models.CharField(max_length=255)
    issue_year = models.IntegerField()
    expiration_date = models.DateField(null=True, blank=True)
    link = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(default="", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{} - {}".format(self.id, self.is_active)

    class Meta:
        verbose_name = "Certificate"
        verbose_name_plural = "Certificates"
        ordering = ['-created_at']


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    instituion = models.CharField(max_length=255)
    course_year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{} - {}".format(self.id, self.is_active)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ['-created_at']


class Achievement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{} - {}".format(self.id, self.is_active)

    class Meta:
        verbose_name = "Achievement"
        verbose_name_plural = "Achievements"
        ordering = ['-created_at']


class ContactData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    link_text = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{} - {}".format(self.id, self.is_active)

    class Meta:
        verbose_name = "Contact Data"
        verbose_name_plural = "Contact Data"
        ordering = ['-created_at']


class ContactForm(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_answered = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Contact Form"
        verbose_name_plural = "Contact Forms"
        ordering = ['-created_at']

    def __str__(self):
        return "{} - {}".format(self.id, self.is_active)


class ContactFormMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contact_form = models.ForeignKey(ContactForm, on_delete=models.CASCADE, related_name='messages')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Contact Form Message"
        verbose_name_plural = "Contact Form Messages"
        ordering = ['-created_at']

    def __str__(self):
        return "{} - {}".format(self.id, self.contact_form)
