from django.db import models
from django.conf import settings
from courses.models import Course

class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Check if the status was changed to approved
        is_new = self.pk is None
        if not is_new:
            old_instance = Application.objects.get(pk=self.pk)
            if old_instance.status != 'approved' and self.status == 'approved':
                # Trigger payment schedule creation
                from payments.models import PaymentSchedule
                PaymentSchedule.create_for_application(self)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.course} ({self.status})"

class ContactMessage(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.full_name} - {self.subject}"
