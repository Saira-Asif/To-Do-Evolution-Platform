from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich import print
import argparse
from datetime import datetime
from typing import Optional
from src.services.todo_service import TodoService
from src.models.todo import TodoStatus


def safe_int_input(console: Console, prompt: str, error_msg: str = "Invalid input. Please enter a valid number.") -> Optional[int]:
    """Safely get integer input from user."""
    try:
        return int(Prompt.ask(prompt))
    except ValueError:
        console.print(f"[red]{error_msg}[/red]")
        return None


def display_todos(console: Console, todo_service: TodoService, status: Optional[TodoStatus] = None):
    """Display todos in a rich table format."""
    todos = todo_service.get_all_todos(status)

    if not todos:
        console.print("[yellow]No todos found.[/yellow]")
        return

    table = Table(title="Your Todos")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Description", style="green")
    table.add_column("Status", style="bold")
    table.add_column("Due Date", style="yellow")
    table.add_column("Created", style="dim")

    for todo in todos:
        status_style = {
            TodoStatus.PENDING: "red",
            TodoStatus.IN_PROGRESS: "yellow",
            TodoStatus.COMPLETED: "green"
        }[todo.status]

        table.add_row(
            str(todo.id) if todo.id else "N/A",
            todo.title,
            todo.description or "",
            f"[{status_style}]{todo.status.value}[/]",
            todo.due_date.strftime("%Y-%m-%d %H:%M") if todo.due_date else "No due date",
            todo.created_at.strftime("%Y-%m-%d %H:%M")
        )

    console.print(table)


def add_todo(console: Console, todo_service: TodoService):
    """Add a new todo."""
    title = Prompt.ask("Enter todo title")
    description = Prompt.ask("Enter description (optional)", default="")
    description = description if description.strip() else None

    due_date_str = Prompt.ask("Enter due date (YYYY-MM-DD HH:MM, optional)", default="")
    due_date = None
    if due_date_str.strip():
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d %H:%M")
        except ValueError:
            console.print("[red]Invalid date format. Using no due date.[/red]")

    try:
        todo = todo_service.create_todo(title, description, due_date)
        console.print(f"[green]Successfully created todo with ID: {todo.id}[/green]")
    except ValueError as e:
        console.print(f"[red]Error creating todo: {e}[/red]")


def update_todo(console: Console, todo_service: TodoService):
    """Update an existing todo."""
    todo_id = safe_int_input(console, "Enter todo ID to update")
    if todo_id is None:
        return

    todo = todo_service.get_todo(todo_id)
    if not todo:
        console.print(f"[red]Todo with ID {todo_id} not found.[/red]")
        return

    title = Prompt.ask(f"Enter new title (current: {todo.title})", default=todo.title)
    description = Prompt.ask(f"Enter new description (current: {todo.description or 'None'})",
                            default=todo.description or "")
    description = description if description != "None" else None

    try:
        updated_todo = todo_service.update_todo(todo_id, title=title, description=description)
        if updated_todo:
            console.print(f"[green]Successfully updated todo with ID: {updated_todo.id}[/green]")
        else:
            console.print(f"[red]Failed to update todo with ID: {todo_id}[/red]")
    except ValueError as e:
        console.print(f"[red]Error updating todo: {e}[/red]")


def delete_todo(console: Console, todo_service: TodoService):
    """Delete a todo."""
    todo_id = safe_int_input(console, "Enter todo ID to delete")
    if todo_id is None:
        return

    success = todo_service.delete_todo(todo_id)
    if success:
        console.print(f"[green]Successfully deleted todo with ID: {todo_id}[/green]")
    else:
        console.print(f"[red]Todo with ID {todo_id} not found.[/red]")


def mark_todo_status(console: Console, todo_service: TodoService):
    """Mark a todo with a new status."""
    todo_id = safe_int_input(console, "Enter todo ID")
    if todo_id is None:
        return

    todo = todo_service.get_todo(todo_id)
    if not todo:
        console.print(f"[red]Todo with ID {todo_id} not found.[/red]")
        return

    console.print("Select new status:")
    console.print("1. Pending")
    console.print("2. In Progress")
    console.print("3. Completed")

    choice = Prompt.ask("Enter choice (1-3)", choices=["1", "2", "3"])

    if choice == "1":
        updated = todo_service.mark_todo_pending(todo_id)
    elif choice == "2":
        updated = todo_service.mark_todo_in_progress(todo_id)
    else:  # choice == "3"
        updated = todo_service.mark_todo_completed(todo_id)

    if updated:
        console.print(f"[green]Successfully updated todo status to: {updated.status.value}[/green]")
    else:
        console.print(f"[red]Failed to update todo status for ID: {todo_id}[/red]")


def show_menu(console: Console, todo_service: TodoService):
    """Show the main menu and handle user input."""
    while True:
        console.print("\n[bright_blue]Todo CLI Application[/bright_blue]")
        console.print("1. List all todos")
        console.print("2. Add new todo")
        console.print("3. Update todo")
        console.print("4. Delete todo")
        console.print("5. Mark todo status")
        console.print("6. List pending todos")
        console.print("7. List completed todos")
        console.print("8. Exit")

        try:
            choice = Prompt.ask("\nEnter your choice (1-8)", choices=["1", "2", "3", "4", "5", "6", "7", "8"])

            if choice == "1":
                display_todos(console, todo_service)
            elif choice == "2":
                add_todo(console, todo_service)
            elif choice == "3":
                update_todo(console, todo_service)
            elif choice == "4":
                delete_todo(console, todo_service)
            elif choice == "5":
                mark_todo_status(console, todo_service)
            elif choice == "6":
                display_todos(console, todo_service, TodoStatus.PENDING)
            elif choice == "7":
                display_todos(console, todo_service, TodoStatus.COMPLETED)
            elif choice == "8":
                console.print("[green]Goodbye![/green]")
                break
        except KeyboardInterrupt:
            console.print("\n[red]Operation cancelled by user.[/red]")
            break
        except Exception as e:
            console.print(f"[red]An unexpected error occurred: {e}[/red]")


def create_cli_app():
    """
    Create the main CLI application for the todo app.
    """
    console = Console()
    todo_service = TodoService()

    def run_app():
        """Run the CLI application."""
        show_menu(console, todo_service)

    return run_app


def main():
    """Main entry point for the CLI application."""
    app = create_cli_app()
    app()


if __name__ == "__main__":
    main()