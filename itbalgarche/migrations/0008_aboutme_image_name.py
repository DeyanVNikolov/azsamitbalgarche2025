# Generated by Django 5.1.7 on 2025-03-29 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itbalgarche', '0007_contactdata_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutme',
            name='image_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
