from django.urls import path
from app.views import (
    home, courses, about, contact,
    blog, testimonials, team, privacy, gallery,
    login, logout, signup, dashboard,
    blog_submit, course_submit, gallery_submit, testimonial_submit, team_member_submit
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
    path('logout/', logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/blog-submit/', blog_submit, name='blog_submit'),
    path('dashboard/course-submit/', course_submit, name='course_submit'),
    path('dashboard/gallery-submit/', gallery_submit, name='gallery_submit'),
    path('dashboard/testimonial-submit/', testimonial_submit, name='testimonial_submit'),
    path('dashboard/team-member-submit/', team_member_submit, name='team_member_submit'),
]
