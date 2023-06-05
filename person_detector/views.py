from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Post, DetectedFace
from .forms import PostForm
from django.http import HttpResponse
# from .ml_models.test import train
from .ml_models.main import open_camera
from .filters import DatabaseFilter, DetectedFilter
from django.conf import settings
from datetime import date
from .resource import DetectedFaceResource
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import Group, User

import os


# def login_page(request):
#     context = {
#         'title': 'Person Detector | Login'
#     }
#     user = None
#     group_name = 'person-detector-user'

#     if request.method == 'POST':
#         username_login = request.POST['username']
#         password_login = request.POST['password']

#         user = authenticate(request, username=username_login, password=password_login)

#         if user is not None:
#             person_detector_group = Group.objects.get(name=group_name)
#             if person_detector_group in user.groups.all():
#                 login(request, user)
#                 return redirect('person_detector:home')
#             else:
#                 messages.error(request, 'Anda tidak memiliki akses')
#                 return redirect('person_detector:login')
#         else:
#             messages.error(request, 'Username atau password anda salah')
#             return redirect('person_detector:login')
    
#     if request.method == 'GET':
#         if request.user.is_authenticated:
#             # logika untuk user
#             return redirect('person_detector:home')
#         else:
#             # logika untuk anonymous
#             return render(request, 'person_detector/login.html', context)

# def person_detector_user_check(user):
#     group_name = 'person-detector-user'
#     group = Group.objects.get(name=group_name)
#     return group in user.groups.all()

@login_required(login_url='login')
# @user_passes_test(person_detector_user_check, login_url=settings.LOGIN_URL_PERSON_DETECTOR, redirect_field_name=None)
def home(request):
    detected = DetectedFace.objects.all().order_by('-id')
    myFilters = DetectedFilter(request.GET, queryset=detected)

    detected = myFilters.qs
    total_data = len(detected) #untuk menghitung jumlah object

    print(request.user.get_all_permissions())

    context = {
        'title' : 'Person Detector | Home',
        'detected': detected,
        'myFilters': myFilters,
        'total_data': total_data
    }

    return render(request, 'person_detector/home.html', context)

@login_required(login_url='login')
def export_detected_dace(reqeust):
    detected_face = DetectedFaceResource()
    dataset = detected_face.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=all_detectted_face_record.csv'
    return response

@login_required(login_url='login')
def cam(request):
    if request.method == 'GET':
        success, error = open_camera()

        if success:
            messages.success(request, 'Camera Has Been Succesfully Opened')
        else:
            messages.error(request, f'Camera Cannot Opened with error: {error}')
    return redirect('person_detector:home')

@login_required(login_url='login')
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

@login_required(login_url='login')
def post_database(request):
    post_person = Post.objects.all() 
    post_form = PostForm(request.POST or None, request.FILES)
    if request.method == "POST":
        if post_form.is_valid():
            name = post_form.cleaned_data['name']
            
            # validasi agar name yang diinput tidak sama dengan name yang sudah ada
            if Post.objects.filter(name=name).exists():
                messages.error(request, f'{name} already exists in the database.')
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
            messages.success(request, f'{name} successfully added')
            return redirect('person_detector:database')
    
    myFilters = DatabaseFilter(request.GET, queryset=post_person)
    post_person = myFilters.qs  
    context = {
        'title': 'Add Database',
        'action': 'Submit',
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

@login_required(login_url='login')
def delete(request, delete_id):
    objcet = Post.objects.get(id = delete_id)
    objcet.delete()
    pesan = 'Data deleted successfully'            
    messages.success(request, pesan)
    return redirect('person_detector:database')

@login_required(login_url='login')
def update(request, update_id):
    post_person = Post.objects.all()
    form = Post.objects.get(id = update_id)
    name = form.name

    if request.method == 'POST' :
        # name = request.POST.get('name')
        if len(request.FILES) != 0:
            if len(form.picture) > 0:
                os.remove(form.picture.path)
            picture = request.FILES['picture']
            form.picture = picture

            ext = picture.name.split('.')[-1] #mendapatkan ekstensi
            filename = f'{name}.{ext}'
            form.picture.name = filename

        
        form.fullName = request.POST.get('fullName')


        form.save()

        messages.success(request, 'Data successfully updated')
        return redirect('person_detector:database')
    
    context = {
        'title': 'Update Database',
        'form': form,
        'action': 'Update',
        'post': post_person,
    }

    return render(request, 'person_detector/update_database.html', context)

@login_required(login_url='login')
def reset_all(request):
    obj = DetectedFace.objects.all()
    obj.delete()

    messages.success(request, f'All detected faces have been successfully deleted.')
    return redirect('person_detector:home')


def gallery(request):
    context = {
        'title': 'Person Detector | Gallery'
    }
    return render(request, 'person_detector/gallery.html', context)