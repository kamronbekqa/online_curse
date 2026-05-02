from rest_framework import serializers
from .models import Application
from courses.serializers import CourseSerializer

class ApplicationSerializer(serializers.ModelSerializer):
    course_detail = CourseSerializer(source='course', read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'user', 'course', 'course_detail', 'status', 'created_at']
        read_only_fields = ['user', 'status', 'created_at']
