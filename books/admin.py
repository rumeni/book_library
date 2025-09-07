from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Admin interface for Book model."""
    
    list_display = ['title', 'author', 'genre', 'isbn', 'publication_date', 'created_at']
    list_filter = ['genre', 'publication_date', 'created_at']
    search_fields = ['title', 'author', 'isbn']
    list_per_page = 25
    ordering = ['-created_at']
