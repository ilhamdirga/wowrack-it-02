from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Post, DetectedFace
from .forms import PostForm
from django.http import HttpResponse
from .ml_models.test import train
from .ml_models.camera import open_camera
from .filters import DatabaseFilter, DetectedFilter
from django.conf import settings

import os

# Create your views here.
def home(request):
    detected = DetectedFace.objects.all()
    myFilters = DetectedFilter(request.GET, queryset=detected)
    detected = myFilters.qs
    total_data = len(detected) #untuk menghitung jumlah object
    context = {
        'title' : 'Person Detector',
        'detected': detected,
        'myFilters': myFilters,
        'total_data': total_data
    }
    return render(request, 'home.html', context)

def cam(request):
    if request.method == 'GET':
        open_camera()
    return redirect('home')

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
    return render(request, 'database.html', context)

def post_database(request):
    post_person = Post.objects.all() 
    post_form = PostForm(request.POST or None, request.FILES)
    if request.method == "POST":
        if post_form.is_valid():
            name = post_form.cleaned_data['name']
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
            return redirect('database')
    
    myFilters = DatabaseFilter(request.GET, queryset=post_person)
    post_person = myFilters.qs  
    context = {
        'title': 'Add Database',
        'post_form': post_form,
        'post': post_person,
        'myFilters': myFilters
    }
    return render(request, 'add_database.html', context)

def train_data(request):
    image_folder = 'static/images/'
    folder = os.path.join(settings.BASE_DIR, image_folder)
    
    train(folder)

    if True:
        messages.success(request, 'Data berhasil ditrain')
        return redirect('database')

def delete(request, delete_id):
    objcet = Post.objects.get(id = delete_id)
    objcet.delete()
    pesan = 'Data berhasil dihapus'            
    messages.success(request, pesan)
    return redirect('database')

def update(request, update_id):
    post_person = Post.objects.all()
    update_data = Post.objects.get(id=update_id)

    if request.method == "POST":
        form_data = PostForm(request.POST, request.FILES, instance=update_data)
        if form_data.is_valid():
            form_data.fields['name'].disabled = True
            form_data.save()
            pesan = 'Data berhasil diupdate'
            messages.success(request, pesan)
            return redirect('database')
    else:
        form_data = PostForm(instance=update_data)
        form_data.fields['name'].disabled = True
    
    context = {
            'title': 'Update Database',
            'post_form': form_data,
            'post': post_person
        }
    return render(request, 'add_database.html', context)


def gallery(request):
    context = {
        'title': 'Person Detector | Gallery'
    }
    return render(request, 'gallery.html', context)