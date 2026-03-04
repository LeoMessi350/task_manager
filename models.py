from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meeting_date = db.Column(db.Date, nullable=False)
    task_description = db.Column(db.Text, nullable=False)
    assigned_to = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    remarks = db.Column(db.Text, default='')
    email_status = db.Column(db.String(20), default='Pending')
    reminder_sent = db.Column(db.String(20), default='')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.id}: {self.task_description[:20]}>'