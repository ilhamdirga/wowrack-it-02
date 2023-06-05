from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Model untuk Camera
class Camera(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, null = True)
    ip_camera = models.CharField(max_length=200, null=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class ListCamera(models.Model):
    name = models.ForeignKey(Camera, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='trash_can_detector', null=True)

    def __str__(self):
        return self.name
    
# Ketika suatu instance Camera ditambahkan oleh user maka satu CamCard akan dibuat secara otomatis
@receiver(post_save, sender=Camera)
def create_camcard(sender, instance, created, **kwargs):
    if created:
        CamCard.objects.create(name=instance)

# Models untuk Card yang digunakan untuk menampung informasi dari object yang dipotret yang ditampilkan di page Home
class CamCard(models.Model):
    name = models.ForeignKey(Camera, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    timestamp = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name.name
    
# Models untuk Gallery 
class Gallery(models.Model):
    name = models.ForeignKey(Camera, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='trash_can_detector', null=True)
    quantity = models.IntegerField(null=True)
    timestamp = models.DateTimeField()
    detected_day = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name.name
    
    def delete(self, *args, **kwargs):
        self.picture.delete()
        super().delete(*args, **kwargs)  