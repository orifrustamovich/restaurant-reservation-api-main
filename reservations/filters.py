import django_filters
from .models import Reservation


class ReservationFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name="reservation_date")
    date_from = django_filters.DateFilter(
        field_name="reservation_date", lookup_expr="gte"
    )
    date_to = django_filters.DateFilter(
        field_name="reservation_date", lookup_expr="lte"
    )
    # __ — related field orqali filter
    restaurant = django_filters.NumberFilter(
        field_name="table__restaurant__id"
    )

    class Meta:
        model = Reservation
        fields = ["status", "date", "date_from", "date_to", "restaurant"]