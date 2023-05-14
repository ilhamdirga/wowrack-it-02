from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('database/', views.database, name='database'),
    path('database/add/', views.post_database, name='add-database'),
    path('database/delete/<int:delete_id>', views.delete, name='delete_data'),
    path('database/update/<int:update_id>', views.update, name='update_data'),
    path('gallery/', views.gallery, name='gallery'),
]

