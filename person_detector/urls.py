from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'person_detector'
urlpatterns = [
    path('', views.home, name='home'),
    # path('login/', views.login_page, name='login'),
    # path('logout/', LogoutView.as_view(next_page='person_detector:login'), name='logout'),
    path('database/', views.database, name='database'),
    path('database/add/', views.post_database, name='add-database'),
    # path('database/train/', views.train_data, name='train_data'),
    path('open/', views.cam, name='open_cam'),
    path('database/delete/<int:delete_id>', views.delete, name='delete_data'),
    path('database/update/<int:update_id>', views.update, name='update_data'),
    path('reset-all-detected-face/', views.reset_all, name='reset-all-detected-face'),
    path('export/', views.export_detected_dace, name='export-detected-face'),
    path('gallery/', views.gallery, name='gallery'),
]

