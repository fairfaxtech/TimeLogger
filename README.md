# TimeLogger

A simple command-line time tracking tool for personal productivity.

## Features

- Start/stop timers for different tasks
- Categorize tasks
- View detailed time reports
- Filter reports by category or date
- Check current session status
- Data persistence with JSON storage

## Usage

### Basic Commands

```bash
# Start tracking a task
python timelogger.py start "Working on project"

# Start with a specific category
python timelogger.py start "Code review" --category development

# Stop current session
python timelogger.py stop

# Check what's currently being tracked
python timelogger.py status
```

### Reports

```bash
# View all sessions
python timelogger.py report

# Filter by category
python timelogger.py report --category development

# View today's sessions only
python timelogger.py report --today

# List recent sessions with IDs
python timelogger.py list

# List only last 5 sessions
python timelogger.py list --limit 5
```

### Data Management

```bash
# Delete a specific session (use list command to see IDs)
python timelogger.py delete 5

# Force delete without confirmation
python timelogger.py delete 5 --force

# Clear all data
python timelogger.py clear

# Clear all data without confirmation
python timelogger.py clear --force
```

## Installation

```bash
pip install -r requirements.txt
```