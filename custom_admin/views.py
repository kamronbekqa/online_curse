from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from applications.models import Application
from courses.models import Course
from users.models import CustomUser
from django.db.models import Sum

def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.role == 'admin')

@user_passes_test(is_admin)
def dashboard(request):
    total_applications = Application.objects.count()
    pending_applications = Application.objects.filter(status='pending').count()
    total_courses = Course.objects.count()
    total_users = CustomUser.objects.count()
    
    recent_applications = Application.objects.all().order_by('-created_at')[:10]
    
    context = {
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'total_courses': total_courses,
        'total_users': total_users,
        'recent_applications': recent_applications,
    }
    return render(request, 'custom_admin/dashboard.html', context)

@user_passes_test(is_admin)
def application_list(request):
    applications = Application.objects.all().order_by('-created_at')
    return render(request, 'custom_admin/applications.html', {'applications': applications})

@user_passes_test(is_admin)
def approve_application(request, pk):
    application = get_object_or_404(Application, pk=pk)
    application.status = 'approved'
    application.save()
    return redirect('custom_admin:dashboard')

@user_passes_test(is_admin)
def reject_application(request, pk):
    application = get_object_or_404(Application, pk=pk)
    application.status = 'rejected'
    application.save()
    return redirect('custom_admin:dashboard')
