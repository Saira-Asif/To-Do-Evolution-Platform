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

interface CreateTaskData {
  title: string;
  description?: string;
}

interface UpdateTaskData {
  title?: string;
  description?: string;
  completed?: boolean;
}

export function useTasks() {
  const queryClient = useQueryClient();

  // Get all tasks
  const tasksQuery = useQuery<Task[]>({
    queryKey: ['tasks'],
    queryFn: async () => {
      const response = await apiClient.get('/tasks');
      return response.json();
    }
  });

  // Create task mutation
  const createTask = useMutation({
    mutationFn: async (taskData: CreateTaskData) => {
      const response = await apiClient.post('/tasks', {
        json: taskData,
      });
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    },
  });

  // Update task mutation
  const updateTask = useMutation({
    mutationFn: async ({ id, ...taskData }: { id: number } & UpdateTaskData) => {
      const response = await apiClient.put(`/tasks/${id}`, {
        json: taskData,
      });
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      // Also invalidate the specific task query if it exists
      queryClient.invalidateQueries({ queryKey: ['task'] });
    },
  });

  // Delete task mutation
  const deleteTask = useMutation({
    mutationFn: async (id: number) => {
      const response = await apiClient.delete(`/tasks/${id}`);
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    },
  });

  // Toggle task completion mutation
  const toggleTaskCompletion = useMutation({
    mutationFn: async ({ id, completed }: { id: number; completed: boolean }) => {
      const response = await apiClient.patch(`/tasks/${id}/complete`, {
        json: { completed: !completed },
      });
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      // Also invalidate the specific task query if it exists
      queryClient.invalidateQueries({ queryKey: ['task'] });
    },
  });

  return {
    tasks: tasksQuery.data,
    isTasksLoading: tasksQuery.isLoading,
    isTasksError: tasksQuery.isError,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion,
  };
}