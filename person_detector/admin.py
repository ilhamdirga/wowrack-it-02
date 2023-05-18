from django.contrib import admin
from .models import Post, DetectedFace
# Register your models here.
admin.site.register(Post)
admin.site.register(DetectedFace)