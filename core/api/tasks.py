from django.core.mail import send_mail as django_send_mail
from django.conf import settings
from celery import shared_task

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@shared_task
def send_mail(subject, otp, recipient_list):
    html_content = render_to_string(
        "emails/otp_email.html",
        {"otp": otp}
    )

    msg = EmailMultiAlternatives(
        subject=subject,
        body=f"Your OTP is {otp}",
        from_email=settings.EMAIL_HOST_USER,
        to=recipient_list,
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()
