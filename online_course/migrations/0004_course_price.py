# Generated by Django 4.0.5 on 2022-07-06 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_course', '0003_courseregistration_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]