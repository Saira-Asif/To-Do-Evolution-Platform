# Quickstart Guide - Console Todo App

## Overview
This guide will help you quickly set up and start using the Console Todo Application.

## Prerequisites
- Python 3.8 or higher
- pip package manager
- Git (for installation from source)

## Installation

### Option 1: Install via pip
```bash
pip install todo-evolution-platform
```

### Option 2: Install from source
```bash
git clone https://github.com/your-org/todo-evolution-platform.git
cd todo-evolution-platform
pip install -e .
```

## Basic Usage

### Starting the Application
```bash
todo-app
```

### Adding a Todo
```bash
todo-app add "Buy groceries"
```

### Listing Todos
```bash
todo-app list
```

### Completing a Todo
```bash
todo-app complete 1
```

### Deleting a Todo
```bash
todo-app delete 1
```

## Configuration

### Default Configuration Location
- Unix/Linux: `~/.config/todo_app/config.json`
- Windows: `%APPDATA%\todo_app\config.json`

### Basic Configuration File
```json
{
  "storage_path": "~/.todo_app/todos.json",
  "default_priority": "medium",
  "display_completed": true,
  "date_format": "YYYY-MM-DD"
}
```

## Command Reference

### Core Commands
- `todo-app add <title>` - Add a new todo item
- `todo-app list` - List all todo items
- `todo-app complete <id>` - Mark a todo as completed
- `todo-app delete <id>` - Delete a todo item
- `todo-app edit <id> <new_title>` - Edit a todo title
- `todo-app clear` - Clear all completed todos

### Advanced Commands
- `todo-app list --completed` - Show only completed todos
- `todo-app list --pending` - Show only pending todos
- `todo-app list --priority <level>` - Filter by priority (low/medium/high)
- `todo-app list --due <date>` - Show todos due by a specific date

## First Steps

1. **Install the application** using one of the methods above
2. **Add your first todo**:
   ```bash
   todo-app add "Learn how to use the Console Todo App"
   ```
3. **List your todos**:
   ```bash
   todo-app list
   ```
4. **Complete your first todo**:
   ```bash
   todo-app complete 1
   ```

## Troubleshooting

### Common Issues
- **Command not found**: Make sure the installation directory is in your PATH
- **Permission errors**: Ensure you have write access to the configuration directory
- **Storage file issues**: Check that the storage path exists and is writable

### Getting Help
```bash
todo-app --help
```

## Next Steps
- Explore advanced filtering options
- Customize your configuration
- Learn about backup and sync options