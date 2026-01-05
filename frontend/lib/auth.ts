// Frontend authentication utilities
// This file contains utilities for handling authentication in the frontend
// Since Better Auth handles the actual authentication, this will contain
// helper functions for token management and user state

export const setAuthToken = (token: string) => {
  localStorage.setItem('auth_token', token);
};

export const getAuthToken = (): string | null => {
  return localStorage.getItem('auth_token');
};

export const removeAuthToken = () => {
  localStorage.removeItem('auth_token');
};

export const isAuthenticated = (): boolean => {
  const token = getAuthToken();
  return !!token;
};