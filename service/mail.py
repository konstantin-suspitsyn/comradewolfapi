import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from core.config import settings


def send_html_mail(html_content: str, email_to: str, subject: str) -> None:
    message = MIMEMultipart("alternative")
    message["From"] = settings.MAIL_DEFAULT_SENDER
    message["To"] = email_to
    message["Subject"] = subject

    # Attach the plain text and HTML parts to the message
    html_part = MIMEText(html_content, "html")
    message.attach(html_part)

    # Connect to the SMTP server
    with smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT) as server:
        server.starttls()  # Secure the connection
        server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)  # Log in to the SMTP server
        server.sendmail(settings.MAIL_DEFAULT_SENDER, email_to, message.as_string())  # Send the email

def send_confirmation_mail(code: str, email_to: str, middle_link: str):
    subject: str = "Код подтверждения"

    html_message: str = f"""Подтвердите свой email и перейдите по ссылке: {settings.PROJECT_HOST}{middle_link}/{code}"""

    send_html_mail(html_message, email_to, subject)

