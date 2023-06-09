from django.db import models

# Create your models here.
class Post(models.Model):
    name = models.CharField(max_length=20)
    date_created = models.DateField(auto_now_add=True)
    picture = models.ImageField(null=True)

    def __str__(self):
        return self.name