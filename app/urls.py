from django.urls import path
from app.views import (
    home, courses, about, contact,
    blog, testimonials, team, privacy, gallery,
    login, signup, dashboard
)


urlpatterns = [
    path('', home, name='home'),
    path('courses/', courses, name='courses'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('blog/', blog, name='blog'),
    path('testimonials/', testimonials, name='testimonials'),
    path('team/', team, name='team'),
    path('privacy/', privacy, name='privacy'),
    path('gallery/', gallery, name='gallery'),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('dashboard/', dashboard, name='dashboard'),  # New dashboard URL
]
