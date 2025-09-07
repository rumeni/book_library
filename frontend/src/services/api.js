import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_BASE_URL}/books/`,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const bookAPI = {
  // List books with filters
  getBooks: (params = {}) => api.get('', { params }),
  
  // Get book details
  getBook: (id) => api.get(`${id}/`),
  
  // Create book
  createBook: (data) => api.post('', data),
  
  // Update book details
  updateBook: (id, data) => api.patch(`${id}/`, data),
  
  // Update books by author
  updateByAuthor: (author, updateData) => 
    api.patch('update-by-author/', { author, update_data: updateData }),
  
  // Get books by author
  getBooksByAuthor: (author) => api.get(`by-author/${author}/`),

  // Delete book
  deleteBook: (id) => api.delete(`${id}/`),

  // Get authors list
  getAuthors: () => api.get('authors/'),

  // Get genres list  
  getGenres: () => api.get('genres/'),
};