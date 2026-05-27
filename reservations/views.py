from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions import IsReservationOwner

from .filters import ReservationFilter
from .models import Reservation
from .serializers import ReservationCreateSerializer, ReservationSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.select_related(
        "customer", "table", "table__restaurant"
    )
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ReservationFilter
    ordering_fields = ["reservation_date", "created_at"]

    def get_serializer_class(self):
        if self.action == "create":
            return ReservationCreateSerializer
        return ReservationSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy", "retrieve"]:
            return [IsAuthenticated(), IsReservationOwner()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        # Admin — hammani ko'radi
        if user.is_staff:
            return super().get_queryset()
        # Owner — o'z restoraniga kelgan bronlarni ko'radi
        if user.role == "owner":
            return super().get_queryset().filter(table__restaurant__owner=user)
        # Customer — faqat o'z bronlarini ko'radi
        return super().get_queryset().filter(customer=user)

    def perform_create(self, serializer):
        # Customer avtomatik qo'shiladi
        serializer.save(customer=self.request.user)

    @action(detail=True, methods=["post"], url_path="cancel")
    def cancel(self, request, pk=None):
        """POST /api/reservations/{id}/cancel/"""
        reservation = self.get_object()
        if not reservation.can_be_cancelled():
            if reservation.is_past():
                return Response(
                    {"error": "Cannot cancel past reservation"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                {"error": f"Cannot cancel {reservation.status} reservation"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        reservation.status = Reservation.Status.CANCELLED
        # update_fields — faqat shu fieldlarni DB ga yozadi
        reservation.save(update_fields=["status", "updated_at"])
        return Response(
            {
                "message": "Reservation cancelled",
                "reservation": ReservationSerializer(reservation).data,
            }
        )

    @action(detail=True, methods=["post"], url_path="confirm")
    def confirm(self, request, pk=None):
        """POST /api/reservations/{id}/confirm/ — faqat owner"""
        reservation = self.get_object()
        if not request.user.is_staff:
            if reservation.table.restaurant.owner != request.user:
                return Response(
                    {"error": "Only restaurant owner can confirm"},
                    status=status.HTTP_403_FORBIDDEN,
                )
        if reservation.status != Reservation.Status.PENDING:
            return Response(
                {"error": "Only pending reservations can be confirmed"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        reservation.status = Reservation.Status.CONFIRMED
        reservation.save(update_fields=["status", "updated_at"])
        return Response({"message": "Reservation confirmed"})
