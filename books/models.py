from django.db import models
from django.core.exceptions import ValidationError
import re
from .constants import ISBN_COMBINED_PATTERN

class Book(models.Model):
    """Book model for library management."""
    
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, db_index=True)
    isbn = models.CharField(max_length=20, blank=True, default='')
    publication_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    genre = models.CharField(max_length=100, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['author']),
            models.Index(fields=['genre']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['isbn'],
                condition=models.Q(isbn__gt=''),
                name='unique_non_empty_isbn'
            )
        ]

    def clean(self):
        """Custom validation for ISBN format and uniqueness."""
        if self.isbn and self.isbn.strip():
            # Remove formatting
            clean_isbn = self.isbn.replace('-', '').replace(' ', '').upper()
            
            # Validate format
            if not re.fullmatch(ISBN_COMBINED_PATTERN, clean_isbn):
                raise ValidationError({'isbn': 'ISBN must be 10 or 13 characters (digits or X for ISBN-10).'})
            
            # Check X position for ISBN-10
            if len(clean_isbn) == 10 and 'X' in clean_isbn[:-1]:
                raise ValidationError({'isbn': "In ISBN-10, 'X' is allowed only as the last character."})
            
            # Check uniqueness
            if Book.objects.filter(isbn=self.isbn).exclude(pk=self.pk).exists():
                raise ValidationError({'isbn': 'This ISBN already exists.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} by {self.author}"
