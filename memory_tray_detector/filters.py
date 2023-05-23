from django import forms
from .models import Camera

import django_filters

class CameraFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        label="Name",
        lookup_expr='icontains',
        # choices=Camera.objects.values_list('name', 'name').distinct(),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Camera
        fields = [
            'name'
        ]

class GalleryFilter(django_filters.FilterSet):
    name = django_filters.ChoiceFilter(
        label="Name",
        choices=Camera.objects.values_list('name', 'name').distinct(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    