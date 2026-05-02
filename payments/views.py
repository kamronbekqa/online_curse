from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import PaymentInstallment

@login_required
def pay_installment(request, installment_id):
    installment = get_object_or_404(PaymentInstallment, id=installment_id, schedule__user=request.user)
    
    if not installment.is_paid:
        installment.is_paid = True
        installment.paid_at = timezone.now()
        installment.save()
        messages.success(request, f"{installment.due_date} dagi to'lov muvaffaqiyatli amalga oshirildi!")
    else:
        messages.info(request, "Bu to'lov allaqachon amalga oshirilgan.")
        
    return redirect('dashboard')
