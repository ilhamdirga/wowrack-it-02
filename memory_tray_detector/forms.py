from django import forms
from .models import Camera

# Form untuk user menambahkan Camera
class AddCameraForm(forms.ModelForm):
    class Meta:
        model = Camera
        fields = [
            'name',
            'description',
            'ip_camera'
        ]

        widgets = {
            'name': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'This field can not be modified'
                }
            ),
            'description': forms.TextInput(
                attrs= {
                    'class': 'form-control'
                }
            ),
            'ip_camera': forms.TextInput(
                attrs= {
                    'class': 'form-control'
                }
            )
        }