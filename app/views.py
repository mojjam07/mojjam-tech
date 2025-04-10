from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from .models import Blog, Course, Gallery, Testimonial

# Basic page views
def home(request):
    return render(request, 'home.html')

def courses(request):
    return render(request, 'courses.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def blog(request):
    return render(request, 'blog.html')

def testimonials(request):
    return render(request, 'testimonials.html')

def team(request):
    return render(request, 'team.html')

def privacy(request):
    return render(request, 'privacy.html')

def gallery(request):
    return render(request, 'gallery.html')

# Authentication views
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            next_url = request.POST.get('next') or 'dashboard'
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'redirect_url': reverse(next_url)
                })
            return redirect(next_url)
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid username or password'
                }, status=400)
            messages.error(request, 'Invalid username or password')
    
    context = {}
    if 'next' in request.GET:
        context['next'] = request.GET['next']
        
    return render(request, 'login.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('home')

# Dashboard views
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def blog_submit(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        Blog.objects.create(
            title=title,
            content=content,
            author=request.user
        )
        messages.success(request, 'Blog post created successfully!')
        return redirect('dashboard')
    return redirect('dashboard')

@login_required
def course_submit(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        Course.objects.create(
            title=title,
            description=description
        )
        messages.success(request, 'Course created successfully!')
        return redirect('dashboard')
    return redirect('dashboard')

@login_required
def gallery_submit(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.FILES.get('image')
        description = request.POST.get('description')
        Gallery.objects.create(
            title=title,
            image=image,
            description=description
        )
        messages.success(request, 'Gallery item added successfully!')
        return redirect('dashboard')
    return redirect('dashboard')

@login_required
def testimonial_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        content = request.POST.get('content')
        rating = request.POST.get('rating')
        Testimonial.objects.create(
            name=name,
            content=content,
            rating=rating
        )
        messages.success(request, 'Testimonial submitted successfully!')
        return redirect('dashboard')
    return redirect('dashboard')
