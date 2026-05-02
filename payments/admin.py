from django.contrib import admin
from .models import PaymentSchedule, PaymentInstallment

class PaymentInstallmentInline(admin.TabularInline):
    model = PaymentInstallment
    extra = 0

@admin.register(PaymentSchedule)
class PaymentScheduleAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'total_amount', 'start_date', 'monthly_payment', 'created_at')
    inlines = [PaymentInstallmentInline]
    search_fields = ('user__username', 'course__title')

@admin.register(PaymentInstallment)
class PaymentInstallmentAdmin(admin.ModelAdmin):
    list_display = ('schedule', 'amount', 'due_date', 'is_paid', 'paid_at')
    list_filter = ('is_paid', 'due_date')
