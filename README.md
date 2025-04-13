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
```

## Installation

```bash
pip install -r requirements.txt
```