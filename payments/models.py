from django.db import models
from django.conf import settings
from courses.models import Course

class PaymentSchedule(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payment_schedules')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='payment_schedules')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField(help_text="Date when the first payment is due (after grace period)")
    monthly_payment = models.DecimalField(max_digits=12, decimal_places=2)
    duration_months = models.IntegerField(default=12)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Schedule for {self.user} - {self.course} ({self.total_amount})"

    @classmethod
    def create_for_application(cls, application):
        from datetime import date, timedelta
        from dateutil.relativedelta import relativedelta
        
        # Avoid circular import if possible, but already imported Course
        course = application.course
        user = application.user
        
        # Calculate start date (1 month grace period)
        start_date = date.today() + relativedelta(months=1)
        
        schedule = cls.objects.create(
            user=user,
            course=course,
            total_amount=course.price,
            start_date=start_date,
            monthly_payment=course.monthly_payment,
            duration_months=course.duration_months
        )
        
        # Create installments
        for i in range(course.duration_months):
            PaymentInstallment.objects.create(
                schedule=schedule,
                amount=course.monthly_payment,
                due_date=start_date + relativedelta(months=i)
            )
        
        return schedule

class PaymentInstallment(models.Model):
    schedule = models.ForeignKey(PaymentSchedule, on_delete=models.CASCADE, related_name='installments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Installment {self.id} for {self.schedule.user} - Due {self.due_date}"
