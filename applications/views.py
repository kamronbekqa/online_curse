from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Application
from courses.models import Course

@login_required
def apply_for_course(request, course_slug):
    if request.method == 'POST':
        course = get_object_or_404(Course, slug=course_slug)
        
        # Check if application already exists
        if Application.objects.filter(user=request.user, course=course).exists():
            messages.warning(request, "Siz bu kursga allaqachon ariza topshirgansiz.")
        else:
            Application.objects.create(user=request.user, course=course)
            messages.success(request, "Arizangiz muvaffaqiyatli yuborildi! Tez orada siz bilan bog'lanamiz.")
            
        return redirect('dashboard')
        
    return redirect('home')
