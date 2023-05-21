from django.db import models

# Create your models here.
class Post(models.Model):
    name = models.CharField(max_length=20)
    fullName = models.CharField(max_length=50)
    date_created = models.DateField(auto_now_add=True)
    picture = models.ImageField(null=True)

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        self.picture.delete()
        super().delete(*args, **kwargs)  

class DetectedFace(models.Model):
    name = models.CharField(max_length=100)
    detected_time = models.DateTimeField()
    detected_day = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.detected_time})"