# Generated by Django 5.1.7 on 2025-03-29 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itbalgarche', '0011_contactform_contactformmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactform',
            name='email',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='contactform',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
