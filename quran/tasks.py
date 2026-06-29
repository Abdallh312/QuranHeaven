from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_daily_email():
    subject = "Daily Update"
    message = "This is your daily update email."
    from_email = 'abdallhshref4@gmail.com'
    recipient_list = ['recipient@example.com']
    send_mail(subject, message, from_email, recipient_list)
