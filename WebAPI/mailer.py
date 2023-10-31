import smtplib
import json


def send_email(subject, message):
    with open('secrets.json', 'r') as f:
        credentials = json.load(f)
    with open('settings.json', 'r') as f:
        settings = json.load(f)

    from_email = credentials['email']
    password = credentials['password']
    to_email = settings['recipient_email']

    with smtplib.SMTP(credentials['smtp_server'], 587) as server:
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, f"Subject: {subject}\n\n{message}")


def format_message(name, email, content):
    return f"MESSAGE RECEIVED FROM: {name}\nWITH EMAIL: {email}\nCONTENT:\n{content}"

def format_subject(email):
    return f"Contact from: {email}"