'use client';

import { useQuery } from '@tanstack/react-query';
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

interface TaskDetailProps {
  taskId: number;
}

export default function TaskDetail({ taskId }: TaskDetailProps) {
  const { data: task, isLoading, error } = useQuery<Task>({
    queryKey: ['task', taskId],
    queryFn: async () => {
      const response = await apiClient.get(`/tasks/${taskId}`);
      return response.json();
    }
  });

  if (isLoading) return <div>Loading task...</div>;
  if (error) return <div>Error loading task: {(error as Error).message}</div>;
  if (!task) return <div>Task not found</div>;

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <div className="flex items-center mb-4">
        <input
          type="checkbox"
          checked={task.completed}
          // onChange would be implemented to toggle completion
          className="h-5 w-5 text-blue-600 rounded"
        />
        <h2 className={`ml-3 text-xl font-bold ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
          {task.title}
        </h2>
      </div>

      {task.description && (
        <div className="mb-4">
          <h3 className="text-sm font-medium text-gray-500">Description</h3>
          <p className={`mt-1 ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
            {task.description}
          </p>
        </div>
      )}

      <div className="grid grid-cols-2 gap-4 text-sm">
        <div>
          <h3 className="text-xs font-medium text-gray-500">Created</h3>
          <p className="text-gray-900">{new Date(task.created_at).toLocaleString()}</p>
        </div>
        <div>
          <h3 className="text-xs font-medium text-gray-500">Updated</h3>
          <p className="text-gray-900">{new Date(task.updated_at).toLocaleString()}</p>
        </div>
      </div>
    </div>
  );
}