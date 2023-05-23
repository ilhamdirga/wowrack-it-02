from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Camera, CamCard, Gallery
from .forms import AddCameraForm
from .filters import CameraFilter, GalleryFilter
from .ml_models.camera import open_camera
from django.conf import settings
# from memory_tray_detector.models import Gallery

import os

# Create your views here.
def home(request):
    cam_card = CamCard.objects.all()
    context = {
        'title': 'Memory Tray Detector | Home',
        'cam_card': cam_card
    }
    return render(request, 'memory_tray_detector/home.html', context)

def camera(request):
    camera = Camera.objects.all()
    total_cam = len(camera)
    myFilters = CameraFilter(request.GET, queryset=camera)
    camera = myFilters.qs
    context = {
        'title': 'Memory Tray Detector : Camera',
        'camera': camera,
        'total_cam': total_cam,
        'myFilters': myFilters
    }
    return render(request, 'memory_tray_detector/camera.html', context)

def open_cam(request):
    if request.method == 'GET':
        # Cek apakah kamera sudah terbuka sebelumnya
        if 'camera_open' in request.session:
            messages.error(request, 'Camera sedang terbuka')
            return redirect('memory_tray_detector:home')

        save_folder = os.path.join(settings.BASE_DIR, 'static', 'images', 'memory_tray_detector')
        request.session['camera_open'] = True
        open_camera(save_folder)
        del request.session['camera_open']  # Hapus status kamera terbuka setelah selesai

    return redirect('memory_tray_detector:home')

def add_camera(request):
    add_form = AddCameraForm(request.POST or None)
    if request.method == 'POST':
        if add_form.is_valid():
            name = add_form.cleaned_data['name']
            ip_camera = add_form.cleaned_data['ip_camera']
            #validasi agar name dan ip camera yang diinput tidak sama dengan name yang sudah ada
            if Camera.objects.filter(name=name).exists():
                messages.error(request, 'Nama sudah ada di database.')
                return redirect('memory_tray_detector:camera')
            elif Camera.objects.filter(ip_camera=ip_camera).exists():
                messages.error(request, 'Alamat IP Camera sudah ada di database.')
                return redirect('memory_tray_detector:camera')
 
            add_form.save()
            messages.success(request, 'Camera berhasil ditambahkan')
            return redirect('memory_tray_detector:camera')
   
    context = {
        'title': 'Add Camera',
        'add_form': add_form
    }
    return render(request, 'memory_tray_detector/add_camera.html', context)

def delete(request, delete_id):
    cam_object = Camera.objects.get(id = delete_id)
    cam_object.delete()
    messages.success(request, 'Camera berhasil dihapus')

    return redirect('memory_tray_detector:camera')

def update(request, update_id):
    cam_update = Camera.objects.get(id = update_id)
    if request.method == 'POST':
        form_cam_update = AddCameraForm(request.POST or None, instance=cam_update)
        form_cam_update.fields['name'].disabled = True
        if form_cam_update.is_valid():
            form_cam_update.save()

            messages.success(request, 'Camera berhasil diupdate')
            return redirect('memory_tray_detector:camera')
    else:
        form_cam_update = AddCameraForm(instance=cam_update)
        form_cam_update.fields['name'].disabled = True
        context = {
            'title': 'Update Camera',
            'add_form': form_cam_update
        }
    return render(request, 'memory_tray_detector/add_camera.html', context)

def gallery(request):
    gall = Gallery.objects.all().order_by('-id')
    total_pic = len(gall)

    myFilters = GalleryFilter(request.GET, queryset=gall)
    gall = myFilters.qs
    context = {
        'title': 'Memory Tray Detector | Gallery',
        'gallery': gall,
        'myFilters':myFilters,
        'total_pic': total_pic
    }
    return render(request, 'memory_tray_detector/gallery.html', context)

def logout(request):
    context = {
        'title': 'Memory Tray Detector | Log Out'
    }
    return render(request, 'memory_tray_detector/logout.html', context)