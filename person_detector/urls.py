from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    # path('video_feed/', views.video_feed, name='video_feed'),
    path('database/', views.database, name='database'),
    path('database/add/', views.post_database, name='add-database'),
    path('database/train/', views.train_data, name='train_data'),
    path('database/open/', views.cam, name='open_cam'),
    path('database/delete/<int:delete_id>', views.delete, name='delete_data'),
    path('database/update/<int:update_id>', views.update, name='update_data'),
    path('gallery/', views.gallery, name='gallery'),
]

