from rest_framework import viewsets, permissions
from .models import PaymentSchedule, PaymentInstallment
from .serializers import PaymentScheduleSerializer, PaymentInstallmentSerializer

class PaymentScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PaymentScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PaymentSchedule.objects.filter(user=self.request.user)

class PaymentInstallmentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PaymentInstallmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PaymentInstallment.objects.filter(schedule__user=self.request.user)
