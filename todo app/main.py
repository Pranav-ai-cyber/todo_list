from gui import display_menu, add_task, view_tasks, mark_complete, mark_task_pending, delete_task, search_tasks, view_statistics, display_weekly_progress_chart, display_monthly_progress_chart, settings_menu
from task import Task
from rich.prompt import IntPrompt, Prompt
from rich.console import Console
from tinydb import TinyDB
import shutil
import json
import hashlib
import datetime
import os

# Set console to UTF-8 on Windows to support Unicode characters
if os.name == 'nt':
    os.system('chcp 65001 >nul')

console = Console()
db = TinyDB('tasks.json')

settings_file = 'config/settings.json'

def load_settings():
    defaults = {"dark_mode": False, "total_points": 0, "gender": None, "username": None, "password_hash": None, "name": None, "email": None, "smtp_server": None, "smtp_port": 587, "smtp_user": None, "smtp_pass": None, "last_report_date": None, "age": None}
    try:
        with open(settings_file, 'r') as f:
            loaded = json.load(f)
            defaults.update(loaded)
    except:
        pass
    return defaults

def save_settings(settings):
    with open(settings_file, 'w') as f:
        json.dump(settings, f)

def save_tasks(tasks):
    # Create backup before saving
    if db.all():
        shutil.copy('tasks.json', 'backup.json')
    db.truncate()
    for task in tasks:
        db.insert(task.to_dict())

def generate_monthly_report(tasks, total_points):
    total = len(tasks)
    completed = sum(1 for t in tasks if t.completed)
    pending = total - completed
    completion_rate = (completed / total * 100) if total else 0
    report = f"Monthly Progress Report\n\n"
    report += f"Total Tasks: {total}\n"
    report += f"Completed: {completed}\n"
    report += f"Pending: {pending}\n"
    report += f"Completion Rate: {completion_rate:.1f}%\n"
    report += f"Total Points Earned: {total_points}\n"
    return report

def send_email(settings, subject, body):
    if not all(settings.get(k) for k in ['email', 'smtp_server', 'smtp_port', 'smtp_user', 'smtp_pass']):
        return False
    import smtplib
    from email.mime.text import MIMEText
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = settings['smtp_user']
    msg['To'] = settings['email']
    try:
        server = smtplib.SMTP(settings['smtp_server'], settings['smtp_port'])
        server.starttls()
        server.login(settings['smtp_user'], settings['smtp_pass'])
        server.sendmail(settings['smtp_user'], settings['email'], msg.as_string())
        server.quit()
        return True
    except Exception as e:
        console.print(f"[red]Failed to send email: {e}[/red]")
        return False

def select_gender():
    console.print("Select your gender:")
    console.print("1. Male")
    console.print("2. Female")
    console.print("3. Other")
    while True:
        try:
            choice = IntPrompt.ask("Choose an option")
            if 1 <= choice <= 3:
                break
            else:
                console.print("[red]Invalid choice. Choose 1, 2, or 3.[/red]")
        except ValueError:
            console.print("[red]Invalid input. Enter a number.[/red]")
    if choice == 1:
        return "male"
    elif choice == 2:
        return "female"
    else:
        return "other"

def main():
    settings = load_settings()
    if not all(settings.get(k) for k in ['name', 'username', 'password_hash', 'email']):
        name = Prompt.ask("Enter your name")
        username = Prompt.ask("Create a username")
        password = Prompt.ask("Create a password", password=True)
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        email = Prompt.ask("Enter your email")
        age = IntPrompt.ask("Enter your age")
        settings.update({'name': name, 'username': username, 'password_hash': password_hash, 'email': email, 'age': age})
        save_settings(settings)
    else:
        username = Prompt.ask("Username")
        password = Prompt.ask("Password", password=True)
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if username != settings['username'] or password_hash != settings['password_hash']:
            console.print("[red]Invalid credentials![/red]")
            return
    total_points = settings['total_points']
    if settings.get('gender') is None:
        gender = select_gender()
        settings['gender'] = gender
        save_settings(settings)
    console.print(f"[bold green]🚀 Welcome {settings['name']}, to your To-Do List App! Let's boost your productivity and achieve your goals! 🌟[/bold green]\n")
    tasks = [Task.from_dict(task_data) for task_data in db.all()]
    # Check for monthly report
    if settings.get('last_report_date'):
        last_report = datetime.datetime.fromisoformat(settings['last_report_date'])
        if (datetime.datetime.now() - last_report).days >= 30:
            report = generate_monthly_report(tasks, total_points)
            if send_email(settings, 'Monthly To-Do Progress Report', report):
                console.print("[green]Monthly report sent to your email![/green]")
                settings['last_report_date'] = datetime.datetime.now().isoformat()
                save_settings(settings)
            else:
                console.print("[yellow]Could not send monthly report. Check email settings.[/yellow]")
    else:
        # First time, set last_report_date
        settings['last_report_date'] = datetime.datetime.now().isoformat()
        save_settings(settings)
    # Check for overdue tasks (incomplete tasks older than 1 day)
    today = datetime.datetime.now().date()
    overdue_tasks = [task for task in tasks if not task.completed and task.created_date and task.created_date.date() < today - datetime.timedelta(days=1)]
    if overdue_tasks:
        from rich.panel import Panel
        overdue_list = "\n".join([f"- {task.description} (Urgency: {task.urgency})" for task in overdue_tasks])
        panel = Panel.fit(
            f"[bold red]⏰ Reminder: You have {len(overdue_tasks)} incomplete task(s) from more than a day ago![/bold red]\n\n{overdue_list}",
            title="Overdue Tasks",
            border_style="red",
            box=ASCII
        )
        console.print(panel)
        console.print("\n")
    while True:
        display_menu(settings)
        try:
            choice = IntPrompt.ask("[bold cyan]Choose an option[/bold cyan]")
            if choice == 1:
                add_task(tasks)
                save_tasks(tasks)
            elif choice == 2:
                view_tasks(tasks)
            elif choice == 3:
                total_points = mark_complete(tasks, total_points, settings)
                settings['total_points'] = total_points
                save_settings(settings)
                save_tasks(tasks)
            elif choice == 4:
                mark_task_pending(tasks)
                save_tasks(tasks)
            elif choice == 5:
                delete_task(tasks)
                save_tasks(tasks)
            elif choice == 6:
                search_tasks(tasks)
            elif choice == 7:
                view_statistics(tasks)
            elif choice == 8:
                display_weekly_progress_chart(tasks)
            elif choice == 9:
                display_monthly_progress_chart(tasks)
            elif choice == 10:
                settings_menu(settings)
                save_settings(settings)
            elif choice == 0:
                console.print("[red]Goodbye! 👋[/red]")
                break
        except KeyboardInterrupt:
            console.print("[red]\nGoodbye! 👋[/red]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    # This app is a cross-platform CLI application that can run on Windows, macOS, Linux, Android (via Termux), and iOS (via a-Shell or iSH).
    main()
