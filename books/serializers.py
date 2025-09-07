from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    """Complete book serializer for detailed operations."""
    
    isbn = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = Book
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class BookListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for book listings."""
    
    class Meta:
        model = Book
        fields = [
            "id", "title", "author", "isbn", 
            "genre", "publication_date", "created_at"
        ]


class BookCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating books."""
    
    isbn = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = Book
        exclude = ["created_at", "updated_at"]