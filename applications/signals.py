from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Application
from payments.models import PaymentSchedule, PaymentInstallment
from dateutil.relativedelta import relativedelta
from datetime import date
from decimal import Decimal

@receiver(post_save, sender=Application)
def create_payment_schedule_on_approval(sender, instance, created, **kwargs):
    if instance.status == 'approved':
        # Check if schedule already exists to prevent duplicates
        if not PaymentSchedule.objects.filter(user=instance.user, course=instance.course).exists():
            
            # Simulated logic: grace period of 2 months after course duration
            total_duration_and_grace = instance.course.duration_months + 2
            start_payment_date = date.today() + relativedelta(months=total_duration_and_grace)
            
            # Create Schedule (12 months by default as in the UI text)
            months_to_pay = 12
            monthly_payment = instance.course.price / months_to_pay
            
            schedule = PaymentSchedule.objects.create(
                user=instance.user,
                course=instance.course,
                total_amount=instance.course.price,
                start_date=start_payment_date,
                monthly_payment=monthly_payment
            )
            
            # Create Installments
            current_due_date = start_payment_date
            for i in range(months_to_pay):
                PaymentInstallment.objects.create(
                    schedule=schedule,
                    amount=monthly_payment,
                    due_date=current_due_date
                )
                current_due_date = current_due_date + relativedelta(months=1)
