from django.shortcuts import render, redirect
# from django.core.paginator import (
#     Paginator,
#     EmptyPage,
#     PageNotAnInteger
# )
from django.contrib import messages
from .models import Post
from .forms import PostForm



from .filters import *

# Create your views here.
def home(request):
    context = {
        'title' : 'Person Detector'
    }
    return render(request, 'home.html', context)

def database(request):
    post_person = Post.objects.all()
    myFilters = DatabaseFilter(request.GET, queryset=post_person)
    post_person = myFilters.qs

    # paginator
    # default_page = 1
    # page = request.GET.get('page', default_page)
    # items_per_page = 3
    # paginator = Paginator(post_person, items_per_page)
    # try:
    #     items_page = paginator.page(page)
    # except PageNotAnInteger:
    #     items_page = paginator.page(default_page)
    # except EmptyPage:
    #     items_page = paginator.page(paginator.num_pages)

    
    total_data = len(post_person)

    context = {
        'title' : 'Person Detector | Database',
        'post': post_person,
        'myFilters': myFilters,
        # 'items_page': items_page,
        'total_data': total_data
    }
    return render(request, 'database.html', context)

def post_database(request):
    post_person = Post.objects.all() 
    post_form = PostForm(request.POST or None, request.FILES)
    if request.method == "POST":
        if post_form.is_valid():
            post_form.save()

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

def delete(request, delete_id):
    objcet = Post.objects.get(id = delete_id)
    objcet.delete()
    pesan = 'Data berhasil dihapus'            
    messages.success(request, pesan)

    return redirect('database')

def update(request, update_id):
    post_person = Post.objects.all()
    update_data = Post.objects.get(id = update_id)
    # data = {
    #     'name': update_data.name,
    #     'files': request.FILES
    # }
    
    # form_data = PostForm(request.POST or None, initial=data, instance=update_data)

    if request.method == "POST":
        form_data = PostForm(request.POST or None, request.FILES, instance=update_data)
        if form_data.is_valid():
            form_data.save()
            pesan = 'Data berhasil diupdate'            
            messages.success(request, pesan)

            return redirect('database')
    else:
        form_data = PostForm(instance=update_data)
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