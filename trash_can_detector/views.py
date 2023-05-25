from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Camera, CamCard, Gallery
from .forms import AddCameraForm
from .filters import CameraFilter, GalleryFilter
from .ml_models.camera import open_camera
from django.conf import settings

import os

# page Home
def home(request):
    # Mengakses semua instance CamCard
    cam_card = CamCard.objects.all()

    context = {
        'title': 'Trash Can Detector | Home',
        'cam_card': cam_card
    }
    return render(request, 'trash_can_detector/home.html', context)

# page camera
def camera(request):
    # Mengakses instance Camera
    camera = Camera.objects.all()

    # Mengimplementasikan filters untuk list camera
    myFilters = CameraFilter(request.GET, queryset=camera)
    camera = myFilters.qs

    total_cam = len(camera) # Menghitung banyaknya camera

    context = {
        'title': 'Trash Can Detector : Camera',
        'camera': camera,
        'total_cam': total_cam,
        'myFilters': myFilters
    }
    return render(request, 'trash_can_detector/camera.html', context)

def open_cam(request, camera_id):
    if request.method == 'GET':
        save_folder = os.path.join(settings.BASE_DIR, 'static', 'images', 'trash_can_detector')

        # Check apakah camera terbuka
        if 'camera_open' in request.session and request.session['camera_open'] == camera_id:
            messages.error(request, 'Camera sedang terbuka')
            return redirect('trash_can_detector:home')

        # Set session variable untuk open camera
        request.session['camera_open'] = camera_id

        open_camera(save_folder, camera_id)

        # Menghapus session setelah camera tertutup
        if 'camera_open' in request.session:
            del request.session['camera_open']

    return redirect('trash_can_detector:home')


# Menambahkan instance Camera
def add_camera(request):
    add_form = AddCameraForm(request.POST or None)
    if request.method == 'POST':
        if add_form.is_valid():
            name = add_form.cleaned_data['name']
            ip_camera = add_form.cleaned_data['ip_camera']

            #validasi agar name dan ip camera yang diinput tidak sama dengan name yang sudah ada
            if Camera.objects.filter(name=name).exists():
                messages.error(request, 'Nama sudah ada di database.')
                return redirect('trash_can_detector:camera')
            elif Camera.objects.filter(ip_camera=ip_camera).exists():
                messages.error(request, 'Alamat IP Camera sudah ada di database.')
                return redirect('trash_can_detector:camera')
 
            add_form.save()

            # messages ketika instance Camera berhasil ditambahkan
            messages.success(request, 'Added Camera Success')
            return redirect('trash_can_detector:camera')
   
    context = {
        'title': 'Add Camera',
        'add_form': add_form
    }
    return render(request, 'trash_can_detector/add_camera.html', context)

# Untuk menghapus instance Camera
def delete(request, delete_id):
    cam_object = Camera.objects.get(id = delete_id)
    cam_object.delete()
    messages.success(request, 'Camera berhasil dihapus')

    return redirect('trash_can_detector:camera')

# Untuk menghapus photo di Gallery
def delete_gallery(request, delete_id):
    gal_object = Gallery.objects.get(id = delete_id)
    gal_object.delete()
    messages.success(request, 'Deleted Success')

    return redirect('trash_can_detector:gallery')

# Untuk Update instance Camera
def update(request, update_id):
    cam_update = Camera.objects.get(id = update_id)
    if request.method == 'POST':
        form_cam_update = AddCameraForm(request.POST or None, instance=cam_update)
        form_cam_update.fields['name'].disabled = True # Agar user tidak diperbolehkan mengupdate field name
        if form_cam_update.is_valid():
            # Validasi agar alamat ip camera yang diupdate tidak sama dengan ip camera yang sudah ada
            ip_camera = form_cam_update.cleaned_data['ip_camera']
            if Camera.objects.filter(ip_camera=ip_camera).exists():
                messages.error(request, 'Alamat IP Camera sudah ada di database.')
                return redirect('trash_can_detector:camera')

            form_cam_update.save()

            messages.success(request, 'Updated Succes')
            return redirect('trash_can_detector:camera')
    else:
        form_cam_update = AddCameraForm(instance=cam_update)
        form_cam_update.fields['name'].disabled = True
        context = {
            'title': 'Update Camera',
            'add_form': form_cam_update
        }
    return render(request, 'trash_can_detector/add_camera.html', context)

# page Gallery
def gallery(request):
    # Untuk mengakses semua instance di Gallery
    gall = Gallery.objects.all().order_by('-id') # diurutkan dari yang paling baru 

    # Mengimplementasikan filters untuk list instance di Gallery
    myFilters = GalleryFilter(request.GET, queryset=gall)
    gall = myFilters.qs

    total_pic = len(gall) # banyaknya instance di Gallery
    context = {
        'title': 'Trash Can Detector | Gallery',
        'gallery': gall,
        'myFilters':myFilters,
        'total_pic': total_pic
    }
    return render(request, 'trash_can_detector/gallery.html', context)

def logout(request):
 context = {
  'title': 'Trash Can Detector | Log Out'
 }
 return render(request, 'trash_can_detector/logout.html', context)