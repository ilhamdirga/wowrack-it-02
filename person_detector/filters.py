import django_filters
from django import forms
from .models import Post

class DatabaseFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='date_created', lookup_expr='gte', label='Start')
    end_date = django_filters.DateFilter(field_name='date_created', lookup_expr='lte', label='End')
    name = django_filters.CharFilter(
        lookup_expr='icontains', 
        label='Name',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Post
        fields = [
            'name'
        ]

        