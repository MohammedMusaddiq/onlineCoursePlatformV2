# Generated by Django 4.0.5 on 2022-07-06 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_course', '0004_course_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseregistration',
            name='paypal_payment_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]