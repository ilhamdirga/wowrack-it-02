from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Post, DetectedFace
from .forms import PostForm
from django.http import HttpResponse
# from .ml_models.test import train
from .ml_models.main import open_camera
from .filters import DatabaseFilter, DetectedFilter
from django.conf import settings
from datetime import date

import os

# Create your views here.
def home(request):
    detected = DetectedFace.objects.all().order_by('-id')
    myFilters = DetectedFilter(request.GET, queryset=detected)

    if not request.GET:
        myFilters.form.initial['detected_time'] = 'today'
        
    detected = myFilters.qs
    total_data = len(detected) #untuk menghitung jumlah object
    context = {
        'title' : 'Person Detector',
        'detected': detected,
        'myFilters': myFilters,
        'total_data': total_data
    }
    return render(request, 'person_detector/home.html', context)

def cam(request):
    if request.method == 'GET':
        success, error = open_camera()

        if success:
            messages.success(request, 'Camera Has Been Succesfully Opened')
        else:
            messages.error(request, f'Camera Cannot Opened with error: {error}')
    return redirect('person_detector:home')

def database(request):
    post_person = Post.objects.all()
    myFilters = DatabaseFilter(request.GET, queryset=post_person)
    post_person = myFilters.qs
    total_data = len(post_person) #untuk menghitung jumlah object
    context = {
        'title' : 'Person Detector | Database',
        'post': post_person,
        'myFilters': myFilters,
        'total_data': total_data
    }
    return render(request, 'person_detector/database.html', context)

def post_database(request):
    post_person = Post.objects.all() 
    post_form = PostForm(request.POST or None, request.FILES)
    if request.method == "POST":
        if post_form.is_valid():
            name = post_form.cleaned_data['name']
            
            # validasi agar name yang diinput tidak sama dengan name yang sudah ada
            if Post.objects.filter(name=name).exists():
                messages.error(request, 'Nama sudah ada di database.')
                return redirect('person_detector:database')

            picture = request.FILES['picture']
            post = post_form.save(commit=False)
            post.picture = picture

            ext = picture.name.split('.')[-1] #mendapatkan ekstensi
            filename = f'{name}.{ext}'
            post.picture.name = filename
            post.save()

            for person in post_person:
                name = person.name
            pesan = name + ' berhasil ditambahkan'            
            messages.success(request, pesan)
            return redirect('person_detector:database')
    
    myFilters = DatabaseFilter(request.GET, queryset=post_person)
    post_person = myFilters.qs  
    context = {
        'title': 'Add Database',
        'post_form': post_form,
        'post': post_person,
        'myFilters': myFilters
    }
    return render(request, 'person_detector/add_database.html', context)

# def train_data(request):
#     image_folder = 'static/images/person_detector/'
#     folder = os.path.join(settings.BASE_DIR, image_folder)
    
#     train(folder)

#     if True:
#         messages.success(request, 'Data berhasil ditrain')
#         return redirect('person_detector:database')

def delete(request, delete_id):
    objcet = Post.objects.get(id = delete_id)
    objcet.delete()
    pesan = 'Data berhasil dihapus'            
    messages.success(request, pesan)
    return redirect('person_detector:database')

def update(request, update_id):
    post_person = Post.objects.all()
    update_data = Post.objects.get(id=update_id)
    if request.method == "POST":
        form_data = PostForm(request.POST, request.FILES, instance=update_data)
        form_data.fields['name'].disabled = True
        if form_data.is_valid():
            # menghapus picture jika sudah ada
            if 'picture' in request.FILES:
                old_picture_path = update_data.picture.path
                if os.path.exists(old_picture_path):
                    os.remove(old_picture_path)
            # Simpan gambar baru
            picture = form_data.cleaned_data['picture']
            update_data.picture = picture
            update_data.save()

            pesan = 'Data berhasil diupdate'
            messages.success(request, pesan)
            return redirect('person_detector:database')
    else:
        form_data = PostForm(instance=update_data)
        form_data.fields['name'].disabled = True
        context = {
                'title': 'Update Database',
                'post_form': form_data,
                'post': post_person
            }
    return render(request, 'person_detector/add_database.html', context)


def gallery(request):
    context = {
        'title': 'Person Detector | Gallery'
    }
    return render(request, 'person_detector/gallery.html', context)