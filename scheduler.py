from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import date, timedelta
from models import Task, db
from email_utils import send_reminder_email
from flask import Flask

def check_and_send_reminders(app: Flask):
    with app.app_context():
        tomorrow = date.today() + timedelta(days=1)
        tasks_due_tomorrow = Task.query.filter(
            Task.end_date == tomorrow,
            Task.reminder_sent != 'Reminder Sent'
        ).all()
        for task in tasks_due_tomorrow:
            send_reminder_email(task)
            task.reminder_sent = 'Reminder Sent'
            db.session.commit()

def start_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=lambda: check_and_send_reminders(app),
        trigger=CronTrigger(hour=8, minute=0),
        id='daily_reminder',
        replace_existing=True
    )
    scheduler.start()
    return scheduler