import random
from django.core.mail import send_mail
from accounts.models import emailOTP
from django.conf import settings

def email_verification(user):
    otp = str(random.randint(100000, 999999))

    otp_obj, created = emailOTP.objects.update_or_create(
    user=user,
    defaults={"otp": otp}
)
    send_mail(
        subject="Your OTP Code",
        message=f"Your verification OTP is: {otp}. It expires in 5 minutes.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
    return otp_obj