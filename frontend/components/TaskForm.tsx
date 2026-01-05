'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { taskCreateSchema, TaskCreateFormValues } from '@/lib/validation';
import { apiClient } from '@/lib/api';

interface TaskFormProps {
  onTaskCreated?: () => void;
}

export default function TaskForm({ onTaskCreated }: TaskFormProps) {
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Set up react-hook-form with zod validation
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<TaskCreateFormValues>({
    resolver: zodResolver(taskCreateSchema),
  });

  const onSubmit = async (data: TaskCreateFormValues) => {
    setLoading(true);
    setError('');

    try {
      // In a real implementation, this would call the API to create a task
      // For now, we'll simulate the API call
      const response = await fetch('/api/tasks', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        reset(); // Reset form after successful submission
        if (onTaskCreated) {
          onTaskCreated(); // Call the callback to refresh the task list
        }
      } else {
        const errorData = await response.json();
        setError(errorData.message || 'Failed to create task');
      }
    } catch (err) {
      setError('An error occurred while creating the task');
      console.error('Task creation error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      {error && (
        <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
          <span className="block sm:inline">{error}</span>
        </div>
      )}

      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700">
          Title
        </label>
        <div className="mt-1">
          <input
            id="title"
            {...register('title')}
            className={`appearance-none block w-full px-3 py-2 border ${
              errors.title ? 'border-red-500' : 'border-gray-300'
            } rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm`}
            placeholder="What needs to be done?"
          />
          {errors.title && (
            <p className="mt-1 text-sm text-red-600">{errors.title.message}</p>
          )}
        </div>
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700">
          Description
        </label>
        <div className="mt-1">
          <textarea
            id="description"
            {...register('description')}
            rows={3}
            className={`appearance-none block w-full px-3 py-2 border ${
              errors.description ? 'border-red-500' : 'border-gray-300'
            } rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm`}
            placeholder="Add details..."
          />
          {errors.description && (
            <p className="mt-1 text-sm text-red-600">{errors.description.message}</p>
          )}
        </div>
      </div>

      <div>
        <button
          type="submit"
          disabled={loading}
          className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
        >
          {loading ? 'Creating task...' : 'Create Task'}
        </button>
      </div>
    </form>
  );
}