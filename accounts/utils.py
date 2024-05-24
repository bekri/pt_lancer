# accounts/utils.py
import secrets
import logging
from django.core.mail import EmailMessage
from .models import User, OneTimePassword
from django.conf import settings

logger = logging.getLogger(__name__)

def generateOTP():
    # Use secrets module for better security
    otp = ''.join(str(secrets.randbelow(10)) for _ in range(6))
    return otp

def send_code_to_user(email):
    Subject = "One time passcode for Email verification "
    otp_code = generateOTP()
    user = User.objects.get(email=email)
    current_site = "ptlancer.com"
    email_body = f"Howdy {user.first_name}, thanks for signing up on {current_site}. Please verify your email using the one time passcode: {otp_code}"
    from_email = settings.DEFAULT_FROM_EMAIL

    # Create OTP object
    OneTimePassword.objects.create(user=user, code=otp_code)

    # Send email
    send_email = EmailMessage(subject=Subject, body=email_body, from_email=from_email, to=[email])
    send_email.send(fail_silently=True)

def send_normal_email(data):
    try:
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            from_email=settings.EMAIL_HOST_USER,
            to=[data['to_email']]
        )
        email.send()
        logger.info(f"Email sent to {data['to_email']}")
    except Exception as e:
        logger.error(f"Failed to send email to {data['to_email']} - {e}")

