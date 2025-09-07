import React, { useState, useEffect, useCallback } from 'react';
import { bookAPI } from '../services/api';

const BookList = ({ onSelectBook, refreshTrigger }) => {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({
    search: '',
    'genre__icontains': '',
    publication_date_from: '',
    publication_date_to: '',
    ordering: '-created_at'
  });

  const fetchBooks = useCallback(async () => {
    setLoading(true);
    try {
      // Filter out empty parameters
      const cleanFilters = Object.fromEntries(
        Object.entries(filters).filter(([key, value]) => value && value.trim() !== '')
      );
      
      const response = await bookAPI.getBooks(cleanFilters);
      setBooks(response.data.results || []);
    } catch (error) {
      console.error('Error fetching books:', error);
      setBooks([]);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    fetchBooks();
  }, [fetchBooks, refreshTrigger]);

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    
    // Convert genre to genre__icontains for responsive filtering
    if (name === 'genre') {
      setFilters(prev => ({ 
        ...prev, 
        'genre__icontains': value
      }));
    } else {
      setFilters(prev => ({ ...prev, [name]: value }));
    }
  };

  return (
    <div className="book-list">
      <h2>Book Library ({books.length})</h2>
      
      {/* Modern Filters */}
      <div className="filters">
        <input
          type="text"
          name="search"
          placeholder="🔍 Search books, authors..."
          value={filters.search}
          onChange={handleFilterChange}
        />
        <input
          type="text"
          name="genre"
          placeholder="📚 Filter by genre..."
          value={filters['genre__icontains']}
          onChange={handleFilterChange}
        />
        <div className="date-filters">
          <div className="date-input-group">
            <label>📅 From:</label>
            <input
              type="date"
              name="publication_date_from"
              value={filters.publication_date_from}
              onChange={handleFilterChange}
            />
          </div>
          <div className="date-input-group">
            <label>📅 To:</label>
            <input
              type="date"
              name="publication_date_to"
              value={filters.publication_date_to}
              onChange={handleFilterChange}
            />
          </div>
        </div>
        <select name="ordering" value={filters.ordering} onChange={handleFilterChange}>
          <option value="-created_at">⏰ Newest First</option>
          <option value="created_at">⏰ Oldest First</option>
          <option value="title">📖 Title A-Z</option>
          <option value="-title">📖 Title Z-A</option>
          <option value="author">👤 Author A-Z</option>
          <option value="-author">👤 Author Z-A</option>
          <option value="-publication_date">📅 Published Recent</option>
          <option value="publication_date">📅 Published Old</option>
        </select>
      </div>

      {/* Book List */}
      {loading ? (
        <div className="loading">Loading books...</div>
      ) : (
        <div className="books">
          {books.length === 0 ? (
            <div className="no-books">
              <p>No books found. Add some books to get started!</p>
            </div>
          ) : (
            books.map(book => (
              <div key={book.id} className="book-card" onClick={() => onSelectBook(book)}>
                <h3>{book.title}</h3>
                <p><strong>Author:</strong> {book.author}</p>
                <p><strong>Genre:</strong> {book.genre || 'N/A'}</p>
                <p><strong>Published:</strong> {book.publication_date || 'N/A'}</p>
                <small>Added: {new Date(book.created_at).toLocaleDateString()}</small>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
};

export default BookList;