import datetime

from django.utils import timezone
from rest_framework import serializers

from restaurants.serializers import RestaurantListSerializer, TableSerializer

from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    """
    Nested serializer for read operations.
    Includes table and restaurant information.
    """

    table_detail = TableSerializer(source="table", read_only=True)
    restaurant_detail = RestaurantListSerializer(
        source="table.restaurant",
        read_only=True,
    )
    customer_email = serializers.EmailField(source="customer.email", read_only=True)

    class Meta:
        model = Reservation
        fields = [
            "id",
            "customer_email",
            "table",
            "table_detail",
            "restaurant_detail",
            "reservation_date",
            "start_time",
            "end_time",
            "party_size",
            "status",
            "special_requests",
            "created_at",
        ]
        read_only_fields = ["id", "customer_email", "status", "created_at"]

    def validate_reservation_date(self, value):
        """
        Prevent reservations for past dates.
        """
        today = timezone.localdate()

        if value < today:
            raise serializers.ValidationError(
                "Reservations cannot be made for past dates."
            )

        return value

    def validate(self, attrs):
        attrs = super().validate(attrs)

        # Start time must be before end time
        if attrs.get("start_time") and attrs.get("end_time"):
            if attrs["start_time"] >= attrs["end_time"]:
                raise serializers.ValidationError(
                    "Start time must be earlier than end time."
                )

        # Prevent reservations for past times on the current day
        if attrs.get("reservation_date") and attrs.get("start_time"):
            reservation_datetime = timezone.make_aware(
                datetime.datetime.combine(
                    attrs["reservation_date"],
                    attrs["start_time"],
                )
            )

            if reservation_datetime <= timezone.now():
                raise serializers.ValidationError(
                    "Reservations must be made for a future date and time."
                )

        # Conflict check
        table = attrs.get("table")
        date = attrs.get("reservation_date")
        start = attrs.get("start_time")
        end = attrs.get("end_time")

        if table and date and start and end:
            existing_reservations = Reservation.objects.filter(
                table=table,
                reservation_date=date,
                status__in=["pending", "confirmed"],
            ).exclude(
                pk=self.instance.pk if self.instance else None
            )

            for reservation in existing_reservations:
                overlap = (
                    reservation.start_time < end
                    and reservation.end_time > start
                )

                if overlap:
                    raise serializers.ValidationError(
                        f"This table is already reserved from "
                        f"{reservation.start_time} to {reservation.end_time}. "
                        f"Please choose another time."
                    )

        # Capacity check
        if table and attrs.get("party_size"):
            if attrs["party_size"] > table.capacity:
                raise serializers.ValidationError(
                    f"This table can accommodate a maximum of "
                    f"{table.capacity} guests."
                )

        return attrs


class ReservationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            "table",
            "reservation_date",
            "start_time",
            "end_time",
            "party_size",
            "special_requests",
        ]

    def validate_reservation_date(self, value):
        """
        Prevent reservations for past dates.
        """
        today = timezone.localdate()

        if value < today:
            raise serializers.ValidationError(
                "Reservations cannot be made for past dates."
            )

        return value

    def validate(self, attrs):
        # Start time must be before end time
        if attrs.get("start_time") and attrs.get("end_time"):
            if attrs["start_time"] >= attrs["end_time"]:
                raise serializers.ValidationError(
                    "Start time must be earlier than end time."
                )

        # Prevent reservations for past times on the current day
        if attrs.get("reservation_date") and attrs.get("start_time"):
            reservation_datetime = timezone.make_aware(
                datetime.datetime.combine(
                    attrs["reservation_date"],
                    attrs["start_time"],
                )
            )

            if reservation_datetime <= timezone.now():
                raise serializers.ValidationError(
                    "Reservations must be made for a future date and time."
                )

        table = attrs.get("table")
        date = attrs.get("reservation_date")
        start = attrs.get("start_time")
        end = attrs.get("end_time")

        if table and date and start and end:
            existing = Reservation.objects.filter(
                table=table,
                reservation_date=date,
                status__in=["pending", "confirmed"],
            )

            for reservation in existing:
                overlap = (
                    reservation.start_time < end
                    and reservation.end_time > start
                )

                if overlap:
                    raise serializers.ValidationError(
                        f"This table is already reserved from "
                        f"{reservation.start_time} to {reservation.end_time}."
                    )

        if table and attrs.get("party_size"):
            if attrs["party_size"] > table.capacity:
                raise serializers.ValidationError(
                    f"This table can accommodate a maximum of "
                    f"{table.capacity} guests."
                )

        return attrs