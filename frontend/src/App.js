import React, { useState, useEffect } from 'react';
import BookList from './components/BookList';
import BookForm from './components/BookForm';
import AuthorActions from './components/AuthorActions';
import { bookAPI } from './services/api';
import { useLocalStorage } from './hooks/useLocalStorage';
import './App.css';

function App() {
  const [selectedBook, setSelectedBook] = useState(null);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [isDarkTheme, setIsDarkTheme] = useLocalStorage('darkTheme', false);

  // Apply theme to document body
  useEffect(() => {
    if (isDarkTheme) {
      document.body.classList.add('dark-theme');
      document.body.classList.remove('light-theme');
    } else {
      document.body.classList.add('light-theme');
      document.body.classList.remove('dark-theme');
    }
  }, [isDarkTheme]);

  const handleBookSave = () => {
    setRefreshTrigger(prev => prev + 1);
    setSelectedBook(null);
    setShowCreateForm(false);
  };

  const handleBookSelect = (book) => {
    setSelectedBook(book);
    setShowCreateForm(false);
  };

  const handleCreateNew = () => {
    setSelectedBook(null);
    setShowCreateForm(true);
  };

  const handleCancel = () => {
    setSelectedBook(null);
    setShowCreateForm(false);
  };

  const handleAuthorUpdate = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  const handleBookDelete = async (bookId) => {
    if (!window.confirm('Are you sure you want to delete this book?')) {
      return;
    }
    
    try {
      await bookAPI.deleteBook(bookId);
      setSelectedBook(null);
      setRefreshTrigger(prev => prev + 1);
      // No success alert - confirmation is enough
    } catch (error) {
      console.error('Error deleting book:', error);
      alert('Error deleting book. Please try again.');
    }
  };

  const toggleTheme = () => {
    setIsDarkTheme(prev => !prev);
  };

  return (
    <div className={`App ${isDarkTheme ? 'dark-theme' : 'light-theme'}`}>
      <header className="app-header">
        <div className="header-content">
          <h1>📚 Book Library Management</h1>
        </div>
        <div className="header-actions">
          <button onClick={toggleTheme} className="btn-theme">
            {isDarkTheme ? '☀️ Light' : '🌙 Dark'}
          </button>
          <button onClick={handleCreateNew} className="btn-add-book">
            + Add New Book
          </button>
        </div>
      </header>

      <div className="app-content">
        <div className="main-section">
          <BookList 
            onSelectBook={handleBookSelect}
            refreshTrigger={refreshTrigger}
          />
        </div>

        <div className="side-section">
          {showCreateForm && (
            <div className="book-details">
              <div className="book-details-header">
                <h3>+ Add New Book</h3>
                <button onClick={handleCancel} className="close-btn">✕</button>
              </div>
              <BookForm 
                mode="create"
                onSave={handleBookSave}
                onCancel={handleCancel}
              />
            </div>
          )}
          
          {selectedBook && (
            <div className="book-details">
              <div className="book-details-header">
                <h3>📖 Book Details</h3>
                <button onClick={handleCancel} className="close-btn">✕</button>
              </div>
              
              <div className="book-info">
                <h4>{selectedBook.title}</h4>
                <div className="book-meta">
                  <p><strong>Author:</strong> {selectedBook.author}</p>
                  <p><strong>ISBN:</strong> {selectedBook.isbn || 'N/A'}</p>
                  <p><strong>Genre:</strong> {selectedBook.genre || 'N/A'}</p>
                  <p><strong>Published:</strong> {selectedBook.publication_date || 'N/A'}</p>
                  {selectedBook.description && (
                    <p><strong>Description:</strong> {selectedBook.description}</p>
                  )}
                </div>
              </div>
              
              <div className="book-actions">
                <button 
                  onClick={() => handleBookDelete(selectedBook.id)}
                  className="btn-danger"
                >
                  🗑️ Delete Book
                </button>
              </div>
              
              <BookForm 
                book={selectedBook}
                mode="edit"
                onSave={handleBookSave}
                onCancel={handleCancel}
              />
            </div>
          )}
          
          <AuthorActions onUpdate={handleAuthorUpdate} />
        </div>
      </div>
    </div>
  );
}

export default App;
