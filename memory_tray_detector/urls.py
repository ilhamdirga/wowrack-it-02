from django.urls import path
from . import views

app_name = 'memory_tray_detector'
urlpatterns = [
    path('', views.home, name='home'),
    path('open-cam/<int:camera_id>/', views.open_cam, name='open-cam'),
    path('camera/', views.camera, name='camera'),
    path('camera/add', views.add_camera, name='add-camera'),
    path('camera/delete/<int:delete_id>', views.delete, name='delete-camera'),
    path('camera/update/<int:update_id>', views.update, name='update-camera'),
    path('gallery/', views.gallery, name='gallery'),
    path('gallery/delete/<int:delete_id>', views.delete_gallery, name='delete-gallery'),
    path('logout/', views.logout, name='logout'),
    
]