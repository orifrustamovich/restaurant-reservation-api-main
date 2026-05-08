import django_filters
from .models import Restaurant, Table


class RestaurantFilter(django_filters.FilterSet):
    # gte = greater than or equal (>=)
    min_rating = django_filters.NumberFilter(
        field_name="rating", lookup_expr="gte"
    )
    max_rating = django_filters.NumberFilter(
        field_name="rating", lookup_expr="lte"
    )

    class Meta:
        model = Restaurant
        fields = ["is_active", "min_rating", "max_rating"]


class TableFilter(django_filters.FilterSet):
    min_capacity = django_filters.NumberFilter(
        field_name="capacity", lookup_expr="gte"
    )

    class Meta:
        model = Table
        fields = ["restaurant", "is_available", "min_capacity"]