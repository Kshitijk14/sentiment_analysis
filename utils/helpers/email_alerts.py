import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText


# Load variables from .env.local
load_dotenv(".env.local")


def send_email_alert(subject, body):
    sender = os.getenv("EMAIL_SENDER")
    recipient = os.getenv("EMAIL_RECIPIENT")
    password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())
