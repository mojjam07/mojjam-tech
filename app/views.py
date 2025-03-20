from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
import json
import logging
from datetime import datetime

# Set up logging
logger = logging.getLogger(__name__)

def home(request):
    current_year = datetime.now().year
    return render(request, 'home.html', {'current_year': current_year})

def courses(request):
    return render(request, 'courses.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Log the received data
        logger.info(f"Received data: {data}")
        return JsonResponse({'message': 'Form submitted successfully!'}, status=201)
    
    return render(request, 'contact.html')

def get_courses(request):
    courses = [
        {"id": 1, "title": "Web Development", "description": "Learn to build dynamic and responsive websites."},
        {"id": 2, "title": "Data Science", "description": "Master the art of data analysis and machine learning."},
        {"id": 3, "title": "Mobile App Development", "description": "Create stunning mobile applications for iOS and Android."},
    ]
    return JsonResponse(courses, safe=False)

@csrf_protect
def create_course(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Here you would typically save the course to the database
        return JsonResponse(data, status=201)

@csrf_protect
def update_course(request, course_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        # Here you would typically update the course in the database
        return JsonResponse(data, status=200)

@csrf_protect
def delete_course(request, course_id):
    if request.method == 'DELETE':
        # Here you would typically delete the course from the database
        return JsonResponse({'message': 'Course deleted'}, status=204)
