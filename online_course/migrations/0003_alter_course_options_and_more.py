# Generated by Django 4.0.5 on 2022-06-29 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('online_course', '0002_rename_courseregiteration_courseregistration_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ('-created_on', '-updated_on'), 'verbose_name_plural': 'Courses'},
        ),
        migrations.AlterModelOptions(
            name='courseregistration',
            options={'ordering': ('-student',), 'verbose_name_plural': 'Course Registrations'},
        ),
    ]
