from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.ImageField(upload_to='category_icons/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Center(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    logo = models.ImageField(upload_to='center_logos/', blank=True, null=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    duration_months = models.IntegerField(help_text="Duration of the course in months")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    center = models.ForeignKey(Center, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    is_popular = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def monthly_payment(self):
        if self.duration_months > 0:
            return self.price / self.duration_months
        return self.price
