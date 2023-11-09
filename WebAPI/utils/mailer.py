import smtplib
import json
from pathlib import Path

class Mailer:
    def __init__(self):
        current_dir = Path(__file__).parent

        settings_path = current_dir / '..' / 'settings.json'

        with open(settings_path, 'r') as f:
            settings = json.load(f)

        self.notification_recipient = settings['recipient_email']
        self.email = settings['email']
        self.password = settings['email_password']
        self.smtpsrv = settings['smtp_server']

    def send(self, subject, message, recipient):
        with smtplib.SMTP(self.smtpsrv, 587) as server:
            server.starttls()
            server.login(self.email, self.password)
            server.sendmail(self.email, recipient, f"Subject: {subject}\n\n{message}")

    def send_notification(self, subject, message):
        self.send(subject, message, self.notification_recipient)

    def send_confirmation(self, recipient):
        with open('confirmation.html', 'r', encoding='utf-8') as file:
            html_content = file.read()
        self.send('Confirmation Email', html_content, recipient)

    def format_message(self, name, email, content):
        return f"MESSAGE RECEIVED FROM: {name}\nWITH EMAIL: {email}\nCONTENT:\n{content}"

    def format_subject(self, email):
        return f"Contact from: {email}"