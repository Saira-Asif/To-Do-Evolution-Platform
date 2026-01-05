from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from models import Task, TaskCreate, TaskPublic, TaskUpdate
from database import get_session
from middleware.auth import get_current_user
from services.task_service import (
    create_task,
    get_tasks_by_user,
    get_task_by_id,
    update_task,
    delete_task,
    toggle_task_completion
)


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/{user_id}/tasks", response_model=TaskPublic)
def create_task_endpoint(
    user_id: str,
    task_create: TaskCreate,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for a user.
    This endpoint creates a new task for the specified user.
    """
    # Verify that the user_id in the URL matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to create tasks for this user")

    # Create the task using the service
    task = create_task(session, user_id, task_create)
    return task


@router.get("/{user_id}/tasks", response_model=List[TaskPublic])
def get_tasks_endpoint(
    user_id: str,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for a user.
    This endpoint returns all tasks associated with the specified user.
    """
    # Verify that the user_id in the URL matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view tasks for this user")

    # Get tasks using the service
    tasks = get_tasks_by_user(session, user_id)
    return tasks


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskPublic)
def get_task_endpoint(
    user_id: str,
    task_id: int,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID.
    This endpoint returns the details of a specific task.
    """
    # Verify that the user_id in the URL matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view tasks for this user")

    # Get the task using the service
    task = get_task_by_id(session, task_id, user_id)
    return task


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskPublic)
def update_task_endpoint(
    user_id: str,
    task_id: int,
    task_update: TaskUpdate,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific task.
    This endpoint updates the details of a specific task.
    """
    # Verify that the user_id in the URL matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update tasks for this user")

    # Update the task using the service
    task = update_task(session, task_id, user_id, task_update)
    return task


@router.delete("/{user_id}/tasks/{task_id}")
def delete_task_endpoint(
    user_id: str,
    task_id: int,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task.
    This endpoint deletes a specific task.
    """
    # Verify that the user_id in the URL matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete tasks for this user")

    # Delete the task using the service
    success = delete_task(session, task_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskPublic)
def toggle_task_completion_endpoint(
    user_id: str,
    task_id: int,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a task.
    This endpoint toggles the completion status of a specific task.
    """
    # Verify that the user_id in the URL matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update tasks for this user")

    # Toggle task completion using the service
    task = toggle_task_completion(session, task_id, user_id)
    return task