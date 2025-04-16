#!/usr/bin/env python3
"""
TimeLogger - A simple command-line time tracking tool
"""

import json
import os
import time
from datetime import datetime
import click

DATA_FILE = 'timelogger_data.json'

def load_data():
    """Load existing data from file"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                # Ensure data structure is valid
                if 'sessions' not in data:
                    data['sessions'] = []
                if 'current_session' not in data:
                    data['current_session'] = None
                return data
        except (json.JSONDecodeError, IOError) as e:
            click.echo(f"Warning: Could not read data file: {e}")
            return {'sessions': [], 'current_session': None}
    return {'sessions': [], 'current_session': None}

def save_data(data):
    """Save data to file"""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        click.echo(f"Error: Could not save data: {e}")
        raise click.Abort()

@click.group()
def cli():
    """TimeLogger - Track your time efficiently"""
    pass

@cli.command()
@click.argument('task', required=False)
@click.option('--category', '-c', default='general', help='Task category')
def start(task, category):
    """Start a new time tracking session"""
    data = load_data()

    if data['current_session']:
        click.echo("Already tracking time! Stop current session first.")
        return

    if not task:
        task = click.prompt('What are you working on?')

    session = {
        'task': task,
        'category': category,
        'start_time': datetime.now().isoformat(),
        'end_time': None
    }

    data['current_session'] = session
    save_data(data)

    click.echo(f"Started tracking: {task} ({category})")

@cli.command()
def stop():
    """Stop the current time tracking session"""
    data = load_data()

    if not data['current_session']:
        click.echo("No active session to stop.")
        return

    current = data['current_session']
    current['end_time'] = datetime.now().isoformat()

    # Calculate duration
    start = datetime.fromisoformat(current['start_time'])
    end = datetime.fromisoformat(current['end_time'])
    duration = (end - start).total_seconds()
    current['duration_seconds'] = duration

    data['sessions'].append(current)
    data['current_session'] = None
    save_data(data)

    hours = int(duration // 3600)
    minutes = int((duration % 3600) // 60)
    click.echo(f"Session stopped. Duration: {hours}h {minutes}m")

@cli.command()
@click.option('--category', '-c', help='Filter by category')
@click.option('--today', is_flag=True, help='Show only today\'s sessions')
def report(category, today):
    """Generate time tracking report"""
    data = load_data()

    if not data['sessions']:
        click.echo("No completed sessions found.")
        return

    sessions = data['sessions']

    # Filter by category if specified
    if category:
        sessions = [s for s in sessions if s['category'] == category]

    # Filter by today if specified
    if today:
        today_date = datetime.now().date()
        sessions = [s for s in sessions if datetime.fromisoformat(s['start_time']).date() == today_date]

    if not sessions:
        click.echo("No sessions match the criteria.")
        return

    # Calculate totals
    total_time = sum(s['duration_seconds'] for s in sessions)
    total_hours = int(total_time // 3600)
    total_minutes = int((total_time % 3600) // 60)

    click.echo(f"\n=== Time Report ===")
    click.echo(f"Total sessions: {len(sessions)}")
    click.echo(f"Total time: {total_hours}h {total_minutes}m")
    click.echo()

    # Group by category
    categories = {}
    for session in sessions:
        cat = session['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(session)

    for cat, cat_sessions in categories.items():
        cat_time = sum(s['duration_seconds'] for s in cat_sessions)
        cat_hours = int(cat_time // 3600)
        cat_minutes = int((cat_time % 3600) // 60)
        click.echo(f"{cat}: {cat_hours}h {cat_minutes}m ({len(cat_sessions)} sessions)")

@cli.command()
def status():
    """Show current tracking status"""
    data = load_data()

    if data['current_session']:
        current = data['current_session']
        start_time = datetime.fromisoformat(current['start_time'])
        elapsed = (datetime.now() - start_time).total_seconds()
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)

        click.echo(f"Currently tracking: {current['task']}")
        click.echo(f"Category: {current['category']}")
        click.echo(f"Elapsed time: {hours}h {minutes}m")
    else:
        click.echo("No active session.")

@cli.command()
@click.option('--limit', '-l', default=10, help='Number of recent sessions to show')
def list(limit):
    """List recent sessions"""
    data = load_data()

    if not data['sessions']:
        click.echo("No completed sessions found.")
        return

    # Get most recent sessions
    recent_sessions = data['sessions'][-limit:]
    recent_sessions.reverse()

    click.echo(f"\n=== Recent Sessions ===")
    for session in recent_sessions:
        start_time = datetime.fromisoformat(session['start_time'])
        duration = session['duration_seconds']
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)

        click.echo(f"{start_time.strftime('%Y-%m-%d %H:%M')} - {session['task']} ({session['category']}) - {hours}h {minutes}m")

if __name__ == '__main__':
    cli()