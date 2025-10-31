from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from rich.box import ASCII
from task import Task
import datetime
import matplotlib.pyplot as plt
import json
import random

console = Console()

motivational_slogans = [
    "🚀 Every small step leads to big achievements. Let's conquer today!",
    "🌟 Your potential is limitless. Start with one task and watch the magic happen!",
    "💪 Believe in yourself! You've got the power to turn dreams into reality.",
    "🔥 Ignite your productivity! Each completed task fuels your success.",
    "🎯 Focus on progress, not perfection. You're unstoppable!",
    "🌈 Embrace challenges; they are the stepping stones to greatness.",
    "⚡ Speed up your success! Tackle tasks with energy and enthusiasm.",
    "🏆 You're a champion in the making. Complete tasks and claim your victory!",
    "💡 Innovation starts with action. Let's create something amazing today!",
    "🌱 Grow through what you go through. Every task completed is a seed of success."
]

low_urgency_slogans = [
    "🌸 Take it easy! Complete these low-priority tasks at your own pace.",
    "🍃 Relax and enjoy the process. These tasks can wait a bit.",
    "🕰️ No rush! Finish these when you have a moment.",
    "🌼 Gentle reminder: These tasks are not urgent, but completing them feels good!"
]

medium_urgency_slogans = [
    "⚖️ Balance is key! Tackle these medium tasks to keep things moving.",
    "🔄 Steady progress: These tasks need attention soon.",
    "📅 Plan ahead! Complete these to stay on track.",
    "🚶‍♂️ Keep walking forward: These medium tasks await your action."
]

high_urgency_slogans = [
    "🚨 Alert! High-priority tasks need immediate action!",
    "🔥 Fire up! These urgent tasks can't wait any longer.",
    "⚡ Lightning speed! Complete these high-urgency items now!",
    "💥 Emergency mode: Dive into these critical tasks right away!"
]

def display_menu(settings):
    slogan = random.choice(motivational_slogans)
    favorite_emoji = "⚽" if settings.get('gender') == 'male' else "💄"
    console.print(f"[bold bright_blue]🌟 Welcome to the Ultimate To-Do List Manager {favorite_emoji} 🌟[/bold bright_blue]")
    console.print(f"[italic bright_yellow]{slogan}[/italic bright_yellow]\n")
    border_style = "white" if settings.get('dark_mode', False) else ("blue" if settings.get('gender') == 'male' else "magenta")
    table = Table(title="[bold bright_white]🚀 Main Menu 🚀[/bold bright_white]", box=ASCII, border_style=border_style, show_header=True, header_style="bold magenta")
    table.add_column("Option", style="cyan", justify="center", no_wrap=True)
    table.add_column("Action", style="magenta", no_wrap=True)
    table.add_row("1", "📝 [bright_green]Add Task[/bright_green]")
    table.add_row("2", "👁️  [bright_cyan]View Tasks[/bright_cyan]")
    table.add_row("3", "✅ [bright_green]Mark Task as Completed[/bright_green]")
    table.add_row("4", "↩️ [bright_yellow]Mark Task as Pending[/bright_yellow]")
    table.add_row("5", "🗑️ [bright_red]Delete Task[/bright_red]")
    table.add_row("6", "🔍 [bright_magenta]Search Tasks[/bright_magenta]")
    table.add_row("7", "📊 [bright_cyan]View Statistics[/bright_cyan]")
    table.add_row("8", "📈 [bright_green]View Daily Progress Chart[/bright_green]")
    table.add_row("9", "📊 [bright_yellow]View Monthly Progress Chart[/bright_yellow]")
    table.add_row("10", "⚙️ [bright_magenta]Settings[/bright_magenta]")
    table.add_row("0", "🚪 [bright_red]Exit[/bright_red]")
    console.print(table)
    console.print("\n[italic bright_black]💡 Tip: Use numbers to navigate the menu. Stay productive! 🚀[/italic bright_black]")

def add_task(tasks):
    description = Prompt.ask("[green]Enter task description[/green]")
    urgency = Prompt.ask("[green]Enter urgency (low/medium/high)[/green]", default="medium")
    task = Task(description, urgency)
    tasks.append(task)
    
    if urgency.lower() == "low":
        slogan = random.choice(low_urgency_slogans)
    elif urgency.lower() == "medium":
        slogan = random.choice(medium_urgency_slogans)
    else:
        slogan = random.choice(high_urgency_slogans)
    
    console.print(f"[green]📝 Task added successfully! {slogan} Description: {description} (Urgency: {urgency})[/green]")

def view_tasks(tasks):
    if not tasks:
        console.print("[yellow]🌟 Your to-do list is empty. Time to add some exciting goals![/yellow]")
        return
    table = Table(title="Your Tasks", box=ASCII)
    table.add_column("No.", style="cyan", justify="center")
    table.add_column("Description", style="magenta")
    table.add_column("Status", style="green")
    table.add_column("Urgency", style="yellow")
    for i, task in enumerate(tasks, 1):
        status = "✅ Completed" if task.completed else "🚧 Pending"
        table.add_row(str(i), task.description, status, task.urgency)
    console.print(table)
    completed_count = sum(1 for task in tasks if task.completed)
    pending_count = len(tasks) - completed_count
    console.print(f"\n[bold cyan]📊 Summary: Total {len(tasks)} tasks | ✅ Completed: {completed_count} | 🚧 Pending: {pending_count}[/bold cyan]")
    
    if pending_count > 0:
        # Find the highest urgency pending task to tailor the motivation
        pending_tasks = [t for t in tasks if not t.completed]
        if pending_tasks:
            max_urgency = max(t.urgency.lower() for t in pending_tasks)
            if max_urgency == "low":
                pending_motivation = random.choice(low_urgency_slogans)
            elif max_urgency == "medium":
                pending_motivation = random.choice(medium_urgency_slogans)
            else:
                pending_motivation = random.choice(high_urgency_slogans)
            console.print(f"\n[bold bright_yellow]💥 {pending_motivation} You've got this – tackle those pending tasks and soar![/bold bright_yellow]")

def mark_complete(tasks, total_points, settings):
    if not tasks:
        console.print("[yellow]No tasks to mark![/yellow]")
        return total_points
    view_tasks(tasks)
    while True:
        try:
            choice_str = Prompt.ask("[blue]Enter task number to mark as completed[/blue]")
            choice = int(choice_str)
            if 1 <= choice <= len(tasks):
                completed_task = tasks[choice - 1]
                completed_task.mark_completed()

                urgency = completed_task.urgency.lower()
                if urgency == "low":
                    slogan = random.choice(low_urgency_slogans)
                elif urgency == "medium":
                    slogan = random.choice(medium_urgency_slogans)
                else:
                    slogan = random.choice(high_urgency_slogans)

                console.print(f"[green]🏆 Fantastic! {slogan} You've conquered '{completed_task.description}'![/green]")

                # Reward system
                base_points = 1 if urgency == 'low' else 3 if urgency == 'medium' else 5
                points = base_points
                if settings.get('age'):
                    age = settings['age']
                    if age < 18:
                        bonus = 2
                    elif 18 <= age <= 30:
                        bonus = 1
                    elif 30 < age <= 50:
                        bonus = 0
                    else:
                        bonus = 1
                    points += bonus
                total_points += points
                if settings.get('age'):
                    console.print(f"[bold bright_green]🎉 Reward: You earned {points} points (base {base_points} + age bonus {bonus})! Total points: {total_points}[/bold bright_green]")
                else:
                    console.print(f"[bold bright_green]🎉 Reward: You earned {points} points! Total points: {total_points}[/bold bright_green]")

                break
            else:
                console.print("[red]Invalid choice. Try again.[/red]")
        except ValueError:
            console.print("[red]Invalid choice. Try again.[/red]")
    return total_points

def mark_task_pending(tasks):
    if not tasks:
        console.print("[yellow]No tasks to mark as pending![/yellow]")
        return
    view_tasks(tasks)
    while True:
        try:
            choice_str = Prompt.ask("[blue]Enter task number to mark as pending[/blue]")
            choice = int(choice_str)
            if 1 <= choice <= len(tasks):
                tasks[choice - 1].mark_pending()
                console.print(f"[green]↩️ Task marked as pending: {tasks[choice - 1].description} Let's get back to it![/green]")
                break
            else:
                console.print("[red]Invalid choice. Try again.[/red]")
        except ValueError:
            console.print("[red]Invalid choice. Try again.[/red]")

def delete_task(tasks):
    if not tasks:
        console.print("[yellow]No tasks to delete![/yellow]")
        return
    view_tasks(tasks)
    while True:
        try:
            choice_str = Prompt.ask("[red]Enter task number to delete[/red]")
            choice = int(choice_str)
            if 1 <= choice <= len(tasks):
                deleted_task = tasks.pop(choice - 1)
                console.print(f"[red]🗑️ Task deleted: {deleted_task.description} It's gone forever![/red]")
                break
            else:
                console.print("[red]Invalid choice. Try again.[/red]")
        except ValueError:
            console.print("[red]Invalid choice. Try again.[/red]")

def search_tasks(tasks):
    if not tasks:
        console.print("[yellow]No tasks to search![/yellow]")
        return
    search_term = Prompt.ask("[cyan]Enter search term[/cyan]").lower()
    matching_tasks = [task for task in tasks if search_term in task.description.lower()]
    if not matching_tasks:
        console.print("[yellow]🔍 No tasks found matching your search.[/yellow]")
        return
    table = Table(title=f"Search Results for '{search_term}'", box=ASCII)
    table.add_column("No.", style="cyan", justify="center")
    table.add_column("Description", style="magenta")
    table.add_column("Status", style="green")
    for i, task in enumerate(matching_tasks, 1):
        status = "✅ Completed" if task.completed else "🚧 Pending"
        table.add_row(str(i), task.description, status)
    console.print(table)

def view_statistics(tasks):
    if not tasks:
        console.print("[yellow]No tasks to analyze![/yellow]")
        return
    total = len(tasks)
    completed = sum(1 for task in tasks if task.completed)
    pending = total - completed
    completion_rate = (completed / total * 100) if total > 0 else 0
    avg_completion_time = None
    if completed > 0:
        times = [task.completed_date - task.created_date for task in tasks if task.completed and task.completed_date and task.created_date]
        if times:
            avg_completion_time = sum(times, datetime.timedelta()) / len(times)
    panel = Panel.fit(
        f"[bold cyan]📊 Task Statistics[/bold cyan]\n\n"
        f"Total Tasks: {total}\n"
        f"✅ Completed: {completed}\n"
        f"🚧 Pending: {pending}\n"
        f"Completion Rate: {completion_rate:.1f}%\n"
        f"Avg Completion Time: {str(avg_completion_time).split('.')[0] if avg_completion_time else 'N/A'}",
        title="Statistics",
        border_style="cyan",
        box=ASCII
    )
    console.print(panel)



def display_weekly_progress_chart(tasks):
    if not tasks:
        console.print("[yellow]No tasks to chart![/yellow]")
        return
    # Get all relevant dates
    dates = set()
    for task in tasks:
        if task.created_date:
            dates.add(task.created_date.date())
        if task.completed and task.completed_date:
            dates.add(task.completed_date.date())
    if not dates:
        console.print("[yellow]No tasks with dates to chart![/yellow]")
        return
    sorted_dates = sorted(dates)
    # Prepare data for plotting
    created_counts = []
    completed_counts = []
    prev_completed_counts = []
    incomplete_counts = []
    for date in sorted_dates:
        created = sum(1 for task in tasks if task.created_date and task.created_date.date() == date)
        completed = sum(1 for task in tasks if task.completed and task.completed_date and task.completed_date.date() == date)
        prev_completed = sum(1 for task in tasks if task.completed and task.completed_date and task.completed_date.date() == date and task.created_date and task.created_date.date() < date)
        incomplete = sum(1 for task in tasks if not task.completed and task.created_date and task.created_date.date() <= date)
        created_counts.append(created)
        completed_counts.append(completed)
        prev_completed_counts.append(prev_completed)
        incomplete_counts.append(incomplete)
    # Plot
    x = range(len(sorted_dates))
    width = 0.2
    plt.bar([i - 1.5*width for i in x], created_counts, width, label='Created', color='blue')
    plt.bar([i - 0.5*width for i in x], completed_counts, width, label='Completed', color='green')
    plt.bar([i + 0.5*width for i in x], prev_completed_counts, width, label='Prev Completed', color='orange')
    plt.bar([i + 1.5*width for i in x], incomplete_counts, width, label='Incomplete', color='red')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.title('Daily Progress Chart')
    plt.xticks(x, [str(d) for d in sorted_dates], rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

def settings_menu(settings):
    console.print("[bold magenta]⚙️ Settings[/bold magenta]\n")
    console.print("1. 🌙 Toggle Dark Mode")
    console.print("2. 📧 Set Email Settings")
    console.print("0. Back to Menu")
    choice = IntPrompt.ask("Choose an option")
    if choice == 1:
        settings['dark_mode'] = not settings['dark_mode']
        console.print(f"[green]Dark mode {'enabled' if settings['dark_mode'] else 'disabled'}[/green]")
    elif choice == 2:
        email = Prompt.ask("Enter your email")
        if '@gmail.com' in email:
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
            smtp_user = email
        elif '@outlook.com' in email or '@hotmail.com' in email:
            smtp_server = 'smtp-mail.outlook.com'
            smtp_port = 587
            smtp_user = email
        else:
            smtp_server = Prompt.ask("SMTP Server")
            smtp_port = IntPrompt.ask("SMTP Port", default=587)
            smtp_user = Prompt.ask("SMTP Username")
        smtp_pass = Prompt.ask("SMTP Password", password=True)
        settings.update({'email': email, 'smtp_server': smtp_server, 'smtp_port': smtp_port, 'smtp_user': smtp_user, 'smtp_pass': smtp_pass})
        console.print("[green]Email settings saved.[/green]")
    elif choice == 0:
        pass
    else:
        console.print("[red]Invalid choice.[/red]")

def display_monthly_progress_chart(tasks):
    if not tasks:
        console.print("[yellow]No tasks to chart![/yellow]")
        return
    # Get all relevant months
    months = set()
    for task in tasks:
        if task.created_date:
            months.add(task.created_date.strftime('%Y-%m'))
        if task.completed and task.completed_date:
            months.add(task.completed_date.strftime('%Y-%m'))
    if not months:
        console.print("[yellow]No tasks with dates to chart![/yellow]")
        return
    sorted_months = sorted(months)
    # Prepare data for plotting
    created_counts = []
    completed_counts = []
    prev_completed_counts = []
    incomplete_counts = []
    for month in sorted_months:
        year, mon = map(int, month.split('-'))
        month_start = datetime.date(year, mon, 1)
        month_end = (month_start + datetime.timedelta(days=31)).replace(day=1) - datetime.timedelta(days=1)
        created = sum(1 for task in tasks if task.created_date and month_start <= task.created_date.date() <= month_end)
        completed = sum(1 for task in tasks if task.completed and task.completed_date and month_start <= task.completed_date.date() <= month_end)
        prev_completed = sum(1 for task in tasks if task.completed and task.completed_date and month_start <= task.completed_date.date() <= month_end and task.created_date and task.created_date.date() < month_start)
        incomplete = sum(1 for task in tasks if not task.completed and task.created_date and task.created_date.date() <= month_end)
        created_counts.append(created)
        completed_counts.append(completed)
        prev_completed_counts.append(prev_completed)
        incomplete_counts.append(incomplete)
    # Plot
    x = range(len(sorted_months))
    width = 0.2
    plt.bar([i - 1.5*width for i in x], created_counts, width, label='Created', color='blue')
    plt.bar([i - 0.5*width for i in x], completed_counts, width, label='Completed', color='green')
    plt.bar([i + 0.5*width for i in x], prev_completed_counts, width, label='Prev Completed', color='orange')
    plt.bar([i + 1.5*width for i in x], incomplete_counts, width, label='Incomplete', color='red')
    plt.xlabel('Month')
    plt.ylabel('Count')
    plt.title('Monthly Progress Chart')
    plt.xticks(x, sorted_months, rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()
