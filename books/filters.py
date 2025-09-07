from django_filters import rest_framework as filters
from .models import Book


class BookFilterSet(filters.FilterSet):
    genre__icontains = filters.CharFilter(field_name='genre', lookup_expr='icontains')
    publication_date_from = filters.DateFilter(field_name='publication_date', lookup_expr='gte')
    publication_date_to = filters.DateFilter(field_name='publication_date', lookup_expr='lte')

    class Meta:
        model = Book
        fields = ['genre__icontains', 'publication_date_from', 'publication_date_to']
