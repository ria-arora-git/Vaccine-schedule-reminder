import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")

def send_reminder(to_email, vaccine_name, due_date):
    print("Preparing to send email...")
    body = f"""
    Vaccine Reminder

    {vaccine_name} is due on {due_date}.

    Please log in to the Vaccine Reminder App and mark it as done after vaccination.
    """

    msg = MIMEText(body)
    msg["Subject"] = "Vaccine Reminder"
    msg["From"] = EMAIL
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL, APP_PASSWORD)
        server.send_message(msg)

    print("Email sent successfully")

