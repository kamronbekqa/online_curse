from django.urls import path
from . import views

urlpatterns = [
    path('apply/<slug:course_slug>/', views.apply_for_course, name='apply_for_course'),
]
