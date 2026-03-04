import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from models import db, Task
from email_utils import init_mail, send_task_email
from scheduler import start_scheduler
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

db.init_app(app)
init_mail(app)

with app.app_context():
    db.create_all()

# Start the reminder scheduler (will be replaced on Render, but keep for local testing)
scheduler = start_scheduler(app)

def parse_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d').date()

@app.route('/')
def index():
    tasks = Task.query.order_by(Task.end_date).all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        task = Task(
            meeting_date=parse_date(request.form['meeting_date']),
            task_description=request.form['task_description'],
            assigned_to=request.form['assigned_to'],
            start_date=parse_date(request.form['start_date']),
            end_date=parse_date(request.form['end_date']),
            priority=request.form['priority'],
            status=request.form['status'],
            email=request.form['email'],
            remarks=request.form['remarks'],
            email_status='Pending'
        )
        db.session.add(task)
        db.session.commit()

        send_task_email(task, new=True)
        task.email_status = 'Sent'
        db.session.commit()

        flash('Task added and email sent!', 'success')
        return redirect(url_for('index'))
    return render_template('task_form.html', task=None)

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.meeting_date = parse_date(request.form['meeting_date'])
        task.task_description = request.form['task_description']
        task.assigned_to = request.form['assigned_to']
        task.start_date = parse_date(request.form['start_date'])
        task.end_date = parse_date(request.form['end_date'])
        task.priority = request.form['priority']
        task.status = request.form['status']
        task.email = request.form['email']
        task.remarks = request.form['remarks']
        db.session.commit()

        send_task_email(task, new=False)
        task.email_status = 'Sent'
        db.session.commit()

        flash('Task updated and email sent!', 'success')
        return redirect(url_for('index'))
    return render_template('task_form.html', task=task)

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted.', 'info')
    return redirect(url_for('index'))

# Add this for Render cron job
@app.route('/cron/send-reminders')
def cron_send_reminders():
    token = request.args.get('token')
    if token != os.getenv('CRON_SECRET'):
        return "Unauthorized", 401
    from scheduler import check_and_send_reminders
    check_and_send_reminders(app)
    return "Reminders sent (if any)."

if __name__ == '__main__':
    app.run(debug=True)