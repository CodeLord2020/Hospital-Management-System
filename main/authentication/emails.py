from django.core.mail import send_mail
from django.conf import settings
import random
from .models import User


def send_otp(email):
    
    subject = "Account Verification Email From HMS"
    otp = random.randint(1000, 9999)
    message = f"Your OTP is {otp}"
    email_from = settings.EMAIL_HOST
    send_mail(subject,message, email_from,[email])
    user_obj = User.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()

def send_appointment_mail(email, date, doc):
    subject = "Appointment Notification Email From HMS"
    message = f"You have a new appointment with Dr.{doc} on {date}"
    email_from = settings.EMAIL_HOST
    send_mail(subject,message, email_from,[email],fail_silently=False)

def send_appointment_change_mail(email, date, doc):
    subject = "Appointment Change Notification Email From HMS"
    message = f"Your Appointment with Dr.{doc} has been changed to {date}"
    email_from = settings.EMAIL_HOST
    send_mail(subject,message, email_from,[email], fail_silently= False)
