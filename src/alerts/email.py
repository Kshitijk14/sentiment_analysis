import smtplib
from email.mime.text import MIMEText
import yaml

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def send_email_alert(subject, body):
    config = load_config()
    
    sender = config["email"]["sender"]
    recipient = config["email"]["recipient"]
    password = config["email"]["password"]

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())
