from django import forms

from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'name',
            'full_name',
            'picture'
        ]
    
        widgets = {
            'name': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Fill with one word and this field can\'t be updated'
                }
            ),
            'full_name': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Fill with your full name'
                }
            ),
        }

        