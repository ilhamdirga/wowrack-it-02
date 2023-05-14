from django import forms

from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'name',
            'picture'
        ]
    
        widgets = {
            'name': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Fill name'
                }
            ),
            'picture': forms.FileInput(
                attrs= {
                    'class': 'form-control',
                    'type': 'file'
                }
            )
        }

        