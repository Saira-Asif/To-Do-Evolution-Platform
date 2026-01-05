import sys
from typing import Optional
from uuid import UUID

import click
from rich.console import Console
from rich.table import Table

from src.models.storage import InMemoryTodoStorage
from src.models.todo import Todo
from src.services.todo_service import TodoService

# Create a global storage instance
storage = InMemoryTodoStorage()
service = TodoService(storage)
console = Console()


@click.group()
def cli():
    """A CLI tool for managing todos."""
    pass


@cli.command()
@click.argument('title', type=str)
@click.option('--desc', default='', help='Description for the task')
def add(title: str, desc: str):
    """Add a new task."""
    try:
        todo = service.add_task(title, desc)
        console.print(f"[green]Added task:[/green] {todo.title} (ID: {todo.id})")
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@cli.command()
def list():
    """List all tasks."""
    todos = service.get_all_tasks()

    if not todos:
        console.print("[yellow]No tasks found.[/yellow]")
        return

    table = Table(title="Todo List")
    table.add_column("ID", style="dim")
    table.add_column("Status", style="bold")
    table.add_column("Title", style="bold")
    table.add_column("Description")
    table.add_column("Created At")

    for todo in todos:
        status = "X" if todo.completed else "O"
        status_style = "green" if todo.completed else "red"
        table.add_row(
            str(todo.id),
            f"[{status_style}]{status}[/{status_style}]",
            todo.title,
            todo.description or "",
            todo.created_at.strftime("%Y-%m-%d %H:%M")
        )

    console.print(table)


@cli.command()
@click.argument('id', type=str)
@click.option('--title', help='New title for the task')
@click.option('--desc', help='New description for the task')
def update(id: str, title: Optional[str], desc: Optional[str]):
    """Update a task."""
    try:
        todo_id = UUID(id)
    except ValueError:
        console.print(f"[red]Error:[/red] Invalid ID format: {id}")
        sys.exit(1)

    # Check if at least one update field is provided
    if title is None and desc is None:
        console.print("[red]Error:[/red] Please provide at least one field to update (--title or --desc)")
        sys.exit(1)

    try:
        updated_todo = service.update_task(todo_id, title, desc)
        if updated_todo:
            console.print(f"[green]Updated task:[/green] {updated_todo.title} (ID: {updated_todo.id})")
        else:
            console.print(f"[red]Error:[/red] Task with ID {id} not found")
            sys.exit(1)
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@cli.command()
@click.argument('id', type=str)
def delete(id: str):
    """Delete a task."""
    try:
        todo_id = UUID(id)
    except ValueError:
        console.print(f"[red]Error:[/red] Invalid ID format: {id}")
        sys.exit(1)

    # Confirm deletion
    confirm = click.confirm(f"Are you sure you want to delete task {id}?")
    if not confirm:
        console.print("[yellow]Deletion cancelled.[/yellow]")
        return

    if service.delete_task(todo_id):
        console.print(f"[green]Deleted task:[/green] {id}")
    else:
        console.print(f"[red]Error:[/red] Task with ID {id} not found")
        sys.exit(1)


@cli.command()
@click.argument('id', type=str)
def complete(id: str):
    """Mark a task as complete."""
    try:
        todo_id = UUID(id)
    except ValueError:
        console.print(f"[red]Error:[/red] Invalid ID format: {id}")
        sys.exit(1)

    todo = service.complete_task(todo_id)
    if todo:
        console.print(f"[green]Marked task as complete:[/green] {todo.title}")
    else:
        console.print(f"[red]Error:[/red] Task with ID {id} not found")
        sys.exit(1)


@cli.command()
@click.argument('id', type=str)
def uncomplete(id: str):
    """Mark a task as incomplete."""
    try:
        todo_id = UUID(id)
    except ValueError:
        console.print(f"[red]Error:[/red] Invalid ID format: {id}")
        sys.exit(1)

    todo = service.uncomplete_task(todo_id)
    if todo:
        console.print(f"[green]Marked task as incomplete:[/green] {todo.title}")
    else:
        console.print(f"[red]Error:[/red] Task with ID {id} not found")
        sys.exit(1)


def main():
    cli()


if __name__ == "__main__":
    main()