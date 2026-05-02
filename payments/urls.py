from django.urls import path
from . import views

urlpatterns = [
    path('pay/<int:installment_id>/', views.pay_installment, name='pay_installment'),
]
