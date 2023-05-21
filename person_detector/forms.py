from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'name',
            'fullName',
            'picture'
        ]
    
        widgets = {
            'name': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Fill with one word and this field can\'t be updated'
                }
            ),
            'fullName': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Fill with your full name'
                }
            ),
        }

        