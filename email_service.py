
import os
import smtplib
from datetime import date, timedelta
from email.message import EmailMessage

from dotenv import load_dotenv
from database import get_deadlines

load_dotenv()


def send_deadline_digest():
    sender_email = os.getenv("SENDER_EMAIL")
    app_password = os.getenv("SENDER_APP_PASSWORD")
    receiver_email = os.getenv("RECEIVER_EMAIL")

    if not sender_email or not app_password or not receiver_email:
        return False, "Email settings are missing in your .env file."

    today = date.today()
    last_day = today + timedelta(days=3)

    # Read tasks from your existing SQLite database
    deadlines = get_deadlines()

    upcoming_tasks = []

    for row in deadlines:
        task_id, task_name, due_date, subject, completed = row

        # Ignore completed tasks
        if completed:
            continue

        if not due_date:
            continue

        try:
            due = date.fromisoformat(str(due_date))
        except ValueError:
            continue

        # Include tasks due today or within the next 3 days
        if today <= due <= last_day:
            upcoming_tasks.append(
                (task_name, due, subject)
            )

    # Create the email
    message = EmailMessage()
    message["Subject"] = "Your Upcoming Deadline Digest"
    message["From"] = sender_email
    message["To"] = receiver_email

    if upcoming_tasks:
        lines = [
            "Hello!",
            "",
            "Here are your pending deadlines for the next 3 days:",
            "",
        ]

        for task_name, due, subject in sorted(
            upcoming_tasks, key=lambda item: item[1]
        ):
            lines.append(f"Task: {task_name}")
            lines.append(f"Subject: {subject or 'General'}")
            lines.append(f"Due date: {due.strftime('%d %b %Y')}")
            lines.append("")

        lines.append("Good luck with your tasks!")
        email_body = "\n".join(lines)
    else:
        email_body = (
            "Hello!\n\n"
            "You have no pending deadlines due today "
            "or within the next 3 days.\n\n"
            "Keep up the good work!"
        )

    message.set_content(email_body)

    # Connect to Gmail and send the email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.send_message(message)

        return True, "Deadline digest email sent successfully!"

    except (smtplib.SMTPException, OSError) as error:
        return False, f"Could not send email: {error}"
