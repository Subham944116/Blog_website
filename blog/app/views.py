from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.
def register(request):
    if request.method == 'POST':
        username=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        newuser=User.objects.create_user(username=email, email=email, password=password, first_name=username)
        newuser.save()
        return redirect('login')
    return render(request,'register.html')
def home(request):
    posts = Post.objects.all().order_by('-date_post')   # latest first
    return render(request, 'home.html', {'posts': posts})
def logout_view(request):
    logout(request)
    return redirect('login')
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')

         
    
    return render(request, 'login.html')  # Make sure you have login.html template

@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('desc')

        # Create post for logged-in user
        Post.objects.create(
            title=title,
            desc=desc,
            author=request.user   # <- IMPORTANT
        )

        
        return redirect('post_list')

    return render(request, 'create_post.html')

@login_required
def post_list(request):
    posts = Post.objects.filter(author=request.user).order_by('-date_post')
    return render(request, 'post_list.html', {'posts': posts})

