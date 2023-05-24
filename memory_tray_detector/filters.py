from django import forms
from .models import Camera, Gallery

import django_filters

# Untuk memfilter list camera
class CameraFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        label="Name",
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Camera
        fields = [
            'name'
        ]

# Untuk memnfilter list photo di Gallery berdasarkan nama Camera dalam bentuk choice
class GalleryFilter(django_filters.FilterSet):
    name = django_filters.ModelChoiceFilter(
        label="Camera",
        queryset=Camera.objects.all(),
        field_name='name',
        to_field_name='id',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Gallery
        fields = ['name']

    