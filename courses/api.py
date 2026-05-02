from rest_framework import viewsets
from .models import Category, Course
from .serializers import CategorySerializer, CourseSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filterset_fields = ['category', 'is_popular']
    search_fields = ['title', 'description']
