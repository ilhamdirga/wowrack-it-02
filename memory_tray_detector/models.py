from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Camera(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50, null=True)
    ip_camera = models.IntegerField(null=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    
@receiver(post_save, sender=Camera)
def create_camcard(sender, instance, created, **kwargs):
    if created:
        CamCard.objects.create(name=instance)

class CamCard(models.Model):
    name = models.ForeignKey(Camera, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name.name
    
class Gallery(models.Model):
    name = models.ForeignKey(Camera, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='memory_tray_detector', null=True)
    quantity = models.IntegerField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name.name