from sqlmodel import Session, select
from models import Task, TaskCreate, TaskUpdate
from fastapi import HTTPException


def create_task(session: Session, user_id: str, task_create: TaskCreate) -> Task:
    """
    Create a new task for a user.
    """
    # Create a new task instance
    task = Task(
        title=task_create.title,
        description=task_create.description,
        completed=task_create.completed,
        user_id=user_id
    )

    # Add to database
    session.add(task)
    session.commit()
    session.refresh(task)

    return task


def get_tasks_by_user(session: Session, user_id: str):
    """
    Get all tasks for a specific user.
    """
    tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
    return tasks


def get_task_by_id(session: Session, task_id: int, user_id: str):
    """
    Get a specific task by its ID and user ID.
    """
    task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == user_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


def update_task(session: Session, task_id: int, user_id: str, task_update: TaskUpdate):
    """
    Update a specific task.
    """
    task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == user_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update task fields if they are provided in the update request
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.completed is not None:
        task.completed = task_update.completed

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_task(session: Session, task_id: int, user_id: str):
    """
    Delete a specific task.
    """
    task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == user_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()
    return True


def toggle_task_completion(session: Session, task_id: int, user_id: str):
    """
    Toggle the completion status of a task.
    """
    task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == user_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Toggle the completion status
    task.completed = not task.completed
    session.add(task)
    session.commit()
    session.refresh(task)
    return task