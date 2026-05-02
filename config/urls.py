from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

# Import API ViewSets
from courses.api import CategoryViewSet, CourseViewSet
from applications.api import ApplicationViewSet
from payments.api import PaymentScheduleViewSet, PaymentInstallmentViewSet

# API Router
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'applications', ApplicationViewSet, basename='application')
router.register(r'payment-schedules', PaymentScheduleViewSet, basename='payment-schedule')
router.register(r'installments', PaymentInstallmentViewSet, basename='installment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('rest_framework.urls')),  # Basic auth for DRF interface
    
    # Frontend URLs
    path('', include('courses.urls')),
    path('auth/', include('users.urls')),
    path('app/', include('applications.urls')),
    path('payments/', include('payments.urls')),
    path('admin-custom/', include('custom_admin.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
