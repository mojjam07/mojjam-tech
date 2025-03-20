from django.urls import path
from app.views import home, courses, about, contact


urlpatterns = [
    path('', home, name='home'),
    path('courses/', courses, name='courses'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
]
