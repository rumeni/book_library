import React, { useState, useEffect } from 'react';
import { bookAPI } from '../services/api';

const BookForm = ({ book, onSave, onCancel, mode = 'create' }) => {
  const [formData, setFormData] = useState({
    title: '',
    author: '',
    isbn: '',
    publication_date: '',
    description: '',
    genre: ''
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (book && mode === 'edit') {
      setFormData({
        title: book.title || '',
        author: book.author || '',
        isbn: book.isbn || '',
        publication_date: book.publication_date || '',
        description: book.description || '',
        genre: book.genre || ''
      });
    }
  }, [book, mode]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      let response;
      
      if (mode === 'create') {
        response = await bookAPI.createBook(formData);
      } else {
        response = await bookAPI.updateBook(book.id, formData);
      }
      
      onSave(response.data);
      
      // Reset form if creating
      if (mode === 'create') {
        setFormData({
          title: '',
          author: '',
          isbn: '',
          publication_date: '',
          description: '',
          genre: ''
        });
      }
    } catch (error) {
      console.error('Error saving book:', error);
      
      let errorMessage = 'Error saving book. Please try again.';
      if (error.response?.data) {
        const errorData = error.response.data;
        if (typeof errorData === 'object') {
          errorMessage = Object.entries(errorData)
            .map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : value}`)
            .join('\n');
        } else {
          errorMessage = errorData;
        }
      }
      
      alert(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="book-form">
      <h3>{mode === 'create' ? 'Add New Book' : 'Edit Book'}</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Title *</label>
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
          />
        </div>
        
        <div className="form-group">
          <label>Author *</label>
          <input
            type="text"
            name="author"
            value={formData.author}
            onChange={handleChange}
            required
          />
        </div>
        
        <div className="form-group">
          <label>ISBN</label>
          <input
            type="text"
            name="isbn"
            value={formData.isbn}
            onChange={handleChange}
            placeholder="978-0123456789"
          />
        </div>
        
        <div className="form-group">
          <label>Publication Date</label>
          <input
            type="date"
            name="publication_date"
            value={formData.publication_date}
            onChange={handleChange}
          />
        </div>
        
        <div className="form-group">
          <label>Genre</label>
          <input
            type="text"
            name="genre"
            value={formData.genre}
            onChange={handleChange}
            placeholder="Fiction, Non-fiction, etc."
          />
        </div>
        
        <div className="form-group">
          <label>Description</label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows="3"
            placeholder="Brief description of the book..."
          />
        </div>
        
        <div className="form-actions">
          <button type="submit" disabled={loading} className="btn-primary">
            {loading ? 'Saving...' : (mode === 'create' ? 'Add Book' : 'Update Book')}
          </button>
          {mode === 'edit' && (
            <button type="button" onClick={onCancel} className="btn-secondary">
              Cancel
            </button>
          )}
        </div>
      </form>
    </div>
  );
};

export default BookForm;