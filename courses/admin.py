from django.contrib import admin
from .models import Center, Category, Course

@admin.register(Center)
class CenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'center', 'price', 'duration_months', 'is_popular')
    list_filter = ('category', 'center', 'is_popular')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description')
