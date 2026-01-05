import { useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api';

interface CreateTaskData {
  title: string;
  description?: string;
}

export function useCreateTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (taskData: CreateTaskData) => {
      const response = await apiClient.post('/tasks', {
        json: taskData,
      });
      return response.json();
    },
    onSuccess: () => {
      // Invalidate and refetch tasks to show the new task
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    },
  });
}