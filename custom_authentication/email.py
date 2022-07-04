from django.contrib.auth import get_user_model
from django.core.mail import send_mail
import random
from django.conf import settings

User = get_user_model()


def send_otp_via_mail(email):
    subject = "You account verification email"
    otp = random.randint(1000, 9999)
    message = f"You OTP is {otp}"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
    user_obj = User.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()