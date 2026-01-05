'use client';

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api';

interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export default function TaskList() {
  const [editingTaskId, setEditingTaskId] = useState<number | null>(null);
  const [editTitle, setEditTitle] = useState('');
  const [editDescription, setEditDescription] = useState('');

  const queryClient = useQueryClient();

  // Fetch tasks
  const { data: tasks, isLoading, error } = useQuery<Task[]>({
    queryKey: ['tasks'],
    queryFn: async () => {
      const response = await apiClient.get('/tasks');
      return response.json();
    }
  });

  // Toggle task completion
  const toggleTaskCompletion = useMutation({
    mutationFn: async ({ taskId, completed }: { taskId: number; completed: boolean }) => {
      const response = await apiClient.patch(`/tasks/${taskId}/complete`, {
        json: { completed: !completed }
      });
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    }
  });

  // Update task
  const updateTask = useMutation({
    mutationFn: async ({ taskId, title, description }: { taskId: number; title: string; description: string }) => {
      const response = await apiClient.put(`/tasks/${taskId}`, {
        json: { title, description }
      });
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      setEditingTaskId(null);
    }
  });

  // Delete task
  const deleteTask = useMutation({
    mutationFn: async (taskId: number) => {
      const response = await apiClient.delete(`/tasks/${taskId}`);
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    }
  });

  if (isLoading) return <div>Loading tasks...</div>;
  if (error) return <div>Error loading tasks: {(error as Error).message}</div>;

  const handleEditClick = (task: Task) => {
    setEditingTaskId(task.id);
    setEditTitle(task.title);
    setEditDescription(task.description || '');
  };

  const handleUpdateTask = (taskId: number) => {
    updateTask.mutate({ taskId, title: editTitle, description: editDescription });
  };

  return (
    <div className="space-y-4">
      {tasks?.map((task) => (
        <div key={task.id} className="bg-white shadow rounded-lg p-4">
          {editingTaskId === task.id ? (
            <div className="space-y-2">
              <input
                type="text"
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
              <textarea
                value={editDescription}
                onChange={(e) => setEditDescription(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                rows={3}
              />
              <div className="flex space-x-2">
                <button
                  onClick={() => handleUpdateTask(task.id)}
                  disabled={updateTask.isPending}
                  className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
                >
                  {updateTask.isPending ? 'Saving...' : 'Save'}
                </button>
                <button
                  onClick={() => setEditingTaskId(null)}
                  className="px-3 py-1 bg-gray-500 text-white rounded hover:bg-gray-600"
                >
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <div className="flex items-start justify-between">
              <div className="flex items-start">
                <input
                  type="checkbox"
                  checked={task.completed}
                  onChange={() => toggleTaskCompletion.mutate({ taskId: task.id, completed: task.completed })}
                  className="h-4 w-4 text-blue-600 rounded mt-1"
                />
                <div className="ml-3">
                  <h3 className={`text-lg ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                    {task.title}
                  </h3>
                  {task.description && (
                    <p className={`${task.completed ? 'line-through text-gray-500' : 'text-gray-600'}`}>
                      {task.description}
                    </p>
                  )}
                </div>
              </div>
              <div className="flex space-x-2">
                <button
                  onClick={() => handleEditClick(task)}
                  className="text-blue-500 hover:text-blue-700"
                >
                  Edit
                </button>
                <button
                  onClick={() => deleteTask.mutate(task.id)}
                  disabled={deleteTask.isPending}
                  className="text-red-500 hover:text-red-700 disabled:opacity-50"
                >
                  {deleteTask.isPending ? 'Deleting...' : 'Delete'}
                </button>
              </div>
            </div>
          )}
        </div>
      ))}
      {(!tasks || tasks.length === 0) && <p>No tasks found.</p>}
    </div>
  );
}