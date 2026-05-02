from rest_framework import serializers
from .models import PaymentSchedule, PaymentInstallment

class PaymentInstallmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentInstallment
        fields = '__all__'

class PaymentScheduleSerializer(serializers.ModelSerializer):
    installments = PaymentInstallmentSerializer(many=True, read_only=True)

    class Meta:
        model = PaymentSchedule
        fields = ['id', 'user', 'course', 'total_amount', 'start_date', 'monthly_payment', 'created_at', 'installments']
