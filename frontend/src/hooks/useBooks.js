import { useState, useEffect, useCallback } from 'react';
import { bookAPI } from '../services/api';

export const useBooks = (initialFilters = {}) => {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    search: '',
    author: '',
    genre: '',
    ordering: '-created_at',
    ...initialFilters
  });

  const fetchBooks = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await bookAPI.getBooks(filters);
      setBooks(response.data.results || []);
    } catch (err) {
      setError('Failed to fetch books');
      console.error('Error fetching books:', err);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  const updateFilters = useCallback((newFilters) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
  }, []);

  const resetFilters = useCallback(() => {
    setFilters({
      search: '',
      author: '',
      genre: '',
      ordering: '-created_at'
    });
  }, []);

  useEffect(() => {
    fetchBooks();
  }, [fetchBooks]);

  return {
    books,
    loading,
    error,
    filters,
    updateFilters,
    resetFilters,
    refetch: fetchBooks
  };
};
