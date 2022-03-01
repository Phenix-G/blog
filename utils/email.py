from django.core.mail import send_mail

from myblog.settings.development import EMAIL_HOST_USER


def send_register_active_email(to_email, username):
    subject = "Blog"
    message = "Here is the message."
    html_message = f"Here is the html message. <a href='http://127.0.0.1:8000/active/{username}'>激活</a>"
    sender = EMAIL_HOST_USER
    receiver = [to_email]
    send_mail(
        subject,
        message,
        sender,
        receiver,
        html_message=html_message,
        fail_silently=False,
    )
