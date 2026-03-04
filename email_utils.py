from flask_mail import Message
from flask import current_app

mail = None

def init_mail(app):
    global mail
    from flask_mail import Mail
    mail = Mail(app)

def send_task_email(task, new=True):
    if not mail:
        return
    action = "created" if new else "updated"
    subject = f"Task {action}: {task.task_description[:30]}"
    recipients = [task.email, current_app.config['MAIL_USERNAME']]
    body = f"""
A task has been {action}.

Task ID: {task.id}
Meeting Date: {task.meeting_date}
Task Description: {task.task_description}
Assigned To: {task.assigned_to}
Start Date: {task.start_date}
End Date (Due): {task.end_date}
Priority: {task.priority}
Status: {task.status}
Remarks: {task.remarks}

Please take necessary action.
"""
    msg = Message(subject, recipients=recipients, body=body)
    try:
        mail.send(msg)
    except Exception as e:
        print(f"Email sending failed: {e}")

def send_reminder_email(task):
    if not mail:
        return
    subject = f"REMINDER: Task due tomorrow: {task.task_description[:30]}"
    recipients = [task.email, current_app.config['MAIL_USERNAME']]
    body = f"""
This is a reminder that the following task is due tomorrow:

Task ID: {task.id}
Meeting Date: {task.meeting_date}
Task Description: {task.task_description}
Assigned To: {task.assigned_to}
Start Date: {task.start_date}
End Date (Due): {task.end_date}
Priority: {task.priority}
Status: {task.status}
Remarks: {task.remarks}

Please complete it on time.
"""
    msg = Message(subject, recipients=recipients, body=body)
    try:
        mail.send(msg)
    except Exception as e:
        print(f"Reminder email failed: {e}")