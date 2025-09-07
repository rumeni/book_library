import React, { useState } from 'react';
import { bookAPI } from '../services/api';

const AuthorActions = ({ onUpdate }) => {
  const [searchAuthor, setSearchAuthor] = useState('');
  const [updateAuthor, setUpdateAuthor] = useState('');
  const [updateData, setUpdateData] = useState({ 
    genre: '', 
    description: '', 
    publication_date: '' 
  });
  const [authorBooks, setAuthorBooks] = useState([]);
  const [hasSearched, setHasSearched] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSearchByAuthor = async (e) => {
    e.preventDefault();
    if (!searchAuthor.trim()) return;

    setLoading(true);
    setHasSearched(true);
    try {
      const response = await bookAPI.getBooks({ 
        search: searchAuthor,
        ordering: '-created_at'
      });
      setAuthorBooks(response.data.results || []);
    } catch (error) {
      console.error('Error fetching books by author:', error);
      setAuthorBooks([]);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateByAuthor = async (e) => {
    e.preventDefault();
    if (!updateAuthor.trim()) return;
    
    // Filter out empty fields
    const fieldsToUpdate = Object.fromEntries(
      Object.entries(updateData).filter(([key, value]) => value.trim() !== '')
    );
    
    if (Object.keys(fieldsToUpdate).length === 0) {
      alert('Please fill at least one field to update.');
      return;
    }
    
    setLoading(true);
    try {
      const response = await bookAPI.updateByAuthor(updateAuthor, fieldsToUpdate);
      alert(response.data.message || 'Books updated successfully!');
      onUpdate(); // Refresh the main book list
      setUpdateAuthor('');
      setUpdateData({ genre: '', description: '', publication_date: '' });
    } catch (error) {
      console.error('Error updating books by author:', error);
      alert('Error updating books. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="author-actions">
      <h3>Author Actions</h3>
      
      {/* Search Books by Author */}
      <div className="action-section">
        <h4>📚 Search Books by Author</h4>
        <form onSubmit={handleSearchByAuthor}>
          <div className="input-group">
            <input
              type="text"
              placeholder="👤 Search by author name..."
              value={searchAuthor}
              onChange={(e) => setSearchAuthor(e.target.value)}
            />
            <button type="submit" disabled={loading} className="btn-search">
              {loading ? '🔄 Searching...' : '🔍 Search'}
            </button>
          </div>
        </form>
        
        {hasSearched && !loading && (
          <div className="author-books">
            {authorBooks.length > 0 ? (
              <>
                <h5>📚 Found {authorBooks.length} book(s):</h5>
                <div className="mini-books dark-results">
                  {authorBooks.map(book => (
                    <div key={book.id} className="mini-book-card">
                      <strong>{book.title}</strong>
                      <p><strong>Author:</strong> {book.author}</p>
                      <div className="book-meta">
                        {book.genre && <span className="genre">📚 {book.genre}</span>}
                        {book.publication_date && (
                          <span className="year">📅 {new Date(book.publication_date).getFullYear()}</span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </>
            ) : (
              <p className="no-results">❌ No books found for "{searchAuthor}"</p>
            )}
          </div>
        )}
      </div>
      
      {/* Update Books by Author */}
      <div className="action-section">
        <h4>✏️ Bulk Update by Author</h4>
        <form onSubmit={handleUpdateByAuthor}>
          <div className="form-group">
            <input
              type="text"
              placeholder="Author name"
              value={updateAuthor}
              onChange={(e) => setUpdateAuthor(e.target.value)}
            />
          </div>
          <div className="form-group">
            <input
              type="text"
              placeholder="New genre (optional)"
              value={updateData.genre}
              onChange={(e) => setUpdateData(prev => ({ ...prev, genre: e.target.value }))}
            />
          </div>
          <div className="form-group">
            <input
              type="date"
              placeholder="Publication date (optional)"
              value={updateData.publication_date}
              onChange={(e) => setUpdateData(prev => ({ ...prev, publication_date: e.target.value }))}
            />
          </div>
          <div className="form-group">
            <textarea
              placeholder="New description (optional)"
              value={updateData.description}
              onChange={(e) => setUpdateData(prev => ({ ...prev, description: e.target.value }))}
              rows="3"
            />
          </div>
          <button type="submit" disabled={loading} className="btn-update">
            {loading ? 'Updating...' : 'Update All Books'}
          </button>
        </form>
        <p className="help-text">
          Fill any field(s) you want to update for all books by the specified author.
        </p>
      </div>
    </div>
  );
};

export default AuthorActions;