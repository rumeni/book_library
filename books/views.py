from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from django.db.models.functions import Lower
from .models import Book
from .serializers import BookSerializer, BookListSerializer, BookCreateSerializer
from .filters import BookFilterSet

# Valid fields for bulk updates
BULK_UPDATE_FIELDS = {'genre', 'description', 'publication_date', 'isbn'}


class BookViewSet(viewsets.ModelViewSet):
    """ViewSet for book management with case-insensitive ordering."""
    
    queryset = Book.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = BookFilterSet
    search_fields = ['title', 'author']
    ordering_fields = ['title', 'author', 'publication_date', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Apply case-insensitive ordering for title and author fields."""
        queryset = super().get_queryset()
        ordering_param = self.request.query_params.get('ordering')
        
        if not ordering_param:
            return queryset.order_by('-created_at')
            
        # Handle case-insensitive ordering for title and author
        if ordering_param in ['title', '-title']:
            desc = ordering_param.startswith('-')
            return queryset.annotate(title_lower=Lower('title')).order_by(
                '-title_lower' if desc else 'title_lower'
            )
        elif ordering_param in ['author', '-author']:
            desc = ordering_param.startswith('-')
            return queryset.annotate(author_lower=Lower('author')).order_by(
                '-author_lower' if desc else 'author_lower'
            )
        elif ordering_param in ['publication_date', '-publication_date', 'created_at', '-created_at']:
            return queryset.order_by(ordering_param)
            
        return queryset.order_by('-created_at')

    def get_serializer_class(self):
        """Dynamic serializer selection."""
        return {
            'list': BookListSerializer,
            'create': BookCreateSerializer,
        }.get(self.action, BookSerializer)

    @action(detail=False, methods=['patch'], url_path='update-by-author')
    def update_by_author(self, request):
        """Bulk update books by author."""
        author = request.data.get('author')
        update_data = request.data.get('update_data', {})
        
        # Simple validation
        if not author or not update_data:
            return Response({'error': 'Author and update_data required'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Filter valid fields
        filtered_data = {k: v for k, v in update_data.items() if k in BULK_UPDATE_FIELDS}
        
        if not filtered_data:
            return Response({'error': 'No valid fields to update'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Update books
        books = Book.objects.filter(author__icontains=author)
        if not books.exists():
            return Response({'error': f'No books found for author: {author}'}, 
                           status=status.HTTP_404_NOT_FOUND)
        
        with transaction.atomic():
            updated_count = books.update(**filtered_data)
        
        return Response({
            'message': f'Updated {updated_count} books by {author}',
            'books': BookListSerializer(books, many=True).data
        })

    @action(detail=False, methods=['get'], url_path='by-author/(?P<author>[^/.]+)')
    def by_author(self, request, author=None):
        if not author:
            return Response({'error': 'Author required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        books = Book.objects.filter(author__icontains=author)
        return Response({
            'author': author, 
            'count': books.count(), 
            'books': BookListSerializer(books, many=True).data
        })