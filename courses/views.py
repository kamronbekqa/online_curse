from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Category, Center

def home(request):
    popular_courses = Course.objects.filter(is_popular=True)[:6]
    return render(request, 'home.html', {'popular_courses': popular_courses})

def course_list(request):
    courses = Course.objects.all()
    categories = Category.objects.all()
    
    # Simple HTMX/Query filtering
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q')
    
    if category_slug:
        courses = courses.filter(category__slug=category_slug)
    
    if search_query:
        courses = courses.filter(title__icontains=search_query)
        
    context = {
        'courses': courses,
        'categories': categories,
        'selected_category': category_slug,
        'search_query': search_query
    }
    
    # Safe fallback to avoid AttributeError if HtmxMiddleware is missing/misconfigured
    is_htmx = getattr(request, "htmx", False)
    
    if is_htmx:
        # HTMX -> Return only the partial with the courses list
        return render(request, 'courses/partials/course_list.html', context)
        
    # Normal -> Return full page
    return render(request, 'courses/course_list.html', context)

def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    return render(request, 'course_detail.html', {'course': course})

def center_list(request):
    centers = Center.objects.all()
    return render(request, 'centers.html', {'centers': centers})

def about_us(request):
    return render(request, 'about.html')

def contact_us(request):
    if request.method == 'POST':
        from applications.models import ContactMessage
        from django.contrib import messages
        
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message_text = request.POST.get('message')
        
        ContactMessage.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            subject=subject,
            message=message_text
        )
        messages.success(request, "Xabaringiz yuborildi! Tez orada siz bilan bog'lanamiz.")
        return redirect('contact_us')
        
    return render(request, 'contact.html')
