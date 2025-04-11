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
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'sessions': [], 'current_session': None}

def save_data(data):
    """Save data to file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

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

if __name__ == '__main__':
    cli()