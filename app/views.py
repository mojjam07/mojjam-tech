from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from .models import Blog, Course, Gallery, Testimonial, TeamMember

# Basic page views
def home(request):
    return render(request, 'home.html')

def courses(request):
    # Get both dummy data and real courses
    dummy_courses = [
        {'title': 'Web Development', 'description': 'Learn full-stack web development...'},
        {'title': 'Data Science', 'description': 'Master data analysis and visualization...'}
    ]
    real_courses = Course.objects.all().order_by('-created_at')
    return render(request, 'courses.html', {
        'dummy_courses': dummy_courses,
        'real_courses': real_courses
    })

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def blog(request):
    # Get both dummy data and real blog posts
    dummy_blogs = [
        {'title': 'Sample Blog 1', 'content': 'This is a sample blog post content...', 'date': 'June 1, 2023'},
        {'title': 'Sample Blog 2', 'content': 'Another example blog post content...', 'date': 'May 15, 2023'}
    ]
    real_blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'blog.html', {
        'dummy_blogs': dummy_blogs,
        'real_blogs': real_blogs
    })

def testimonials(request):
    # Get both dummy data and real testimonials
    dummy_testimonials = [
        {'name': 'John Doe', 'content': 'Great service!', 'rating': 5},
        {'name': 'Jane Smith', 'content': 'Very helpful', 'rating': 4}
    ]
    real_testimonials = Testimonial.objects.all().order_by('-created_at')
    return render(request, 'testimonials.html', {
        'dummy_testimonials': dummy_testimonials,
        'real_testimonials': real_testimonials
    })

def team(request):
    instructors = TeamMember.objects.filter(role='Instructor').order_by('-created_at')
    support_staff = TeamMember.objects.filter(role='Support Staff').order_by('-created_at')
    return render(request, 'team.html', {
        'instructors': instructors,
        'support_staff': support_staff
    })

def privacy(request):
    return render(request, 'privacy.html')

def gallery(request):
    # Get both dummy data and real gallery items
    dummy_gallery = [
        {'title': 'Event 1', 'description': 'Our first event'},
        {'title': 'Workshop', 'description': 'Learning session'}
    ]
    real_gallery = Gallery.objects.all().order_by('-uploaded_at')
    return render(request, 'gallery.html', {
        'dummy_gallery': dummy_gallery,
        'real_gallery': real_gallery
    })

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
        image = request.FILES.get('image')
        Blog.objects.create(
            title=title,
            content=content,
            image=image,
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
        image = request.FILES.get('image')
        
        if not image:
            messages.error(request, 'Please select an image for the course')
            return redirect('dashboard')
            
        try:
            Course.objects.create(
                title=title,
                description=description,
                image=image
            )
            messages.success(request, 'Course created successfully!')
        except Exception as e:
            messages.error(request, f'Error creating course: {str(e)}')
            
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
        image = request.FILES.get('image')
        Testimonial.objects.create(
            name=name,
            content=content,
            rating=rating,
            image=image
        )
        messages.success(request, 'Testimonial submitted successfully!')
        return redirect('dashboard')
    return redirect('dashboard')

@login_required
def team_member_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        role = request.POST.get('role')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        if not name or not role:
            messages.error(request, 'Name and Role are required fields.')
            return redirect('dashboard')
        TeamMember.objects.create(
            name=name,
            role=role,
            description=description,
            image=image
        )
        messages.success(request, 'Team member added successfully!')
        return redirect('dashboard')
    return redirect('dashboard')
