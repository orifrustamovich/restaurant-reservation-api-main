from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Restaurant, Table
from .serializers import (
    RestaurantSerializer,
    RestaurantListSerializer,
    TableSerializer,
)
from .filters import RestaurantFilter, TableFilter
from users.permissions import IsOwner, IsOwnerOrReadOnly


class RestaurantViewSet(viewsets.ModelViewSet):
    # select_related — JOIN, N+1 query muammosini hal qiladi
    queryset = Restaurant.objects.filter(
        is_active=True
    ).select_related("owner")

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = RestaurantFilter
    search_fields = ["name", "address", "description"]
    ordering_fields = ["name", "rating", "created_at"]

    def get_serializer_class(self):
        if self.action == "list":
            return RestaurantListSerializer  # yengil
        return RestaurantSerializer          # to'liq

    def get_permissions(self):
        """Action ga qarab permission tanlash"""
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticatedOrReadOnly()]
        elif self.action == "create":
            return [IsOwner()]
        return [IsOwnerOrReadOnly()]

    def perform_create(self, serializer):
        # Owner avtomatik qo'shiladi — request dan olinadi
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["get"], url_path="tables")
    def tables(self, request, pk=None):
        """GET /api/restaurants/{id}/tables/"""
        restaurant = self.get_object()
        tables = restaurant.tables.all()
        capacity = request.query_params.get("min_capacity")
        if capacity:
            tables = tables.filter(capacity__gte=capacity)
        return Response(TableSerializer(tables, many=True).data)

    @action(
        detail=False,
        methods=["get"],
        url_path="my-restaurants",
        permission_classes=[IsOwner],
    )
    def my_restaurants(self, request):
        """GET /api/restaurants/my-restaurants/"""
        restaurants = Restaurant.objects.filter(owner=request.user)
        return Response(
            RestaurantListSerializer(restaurants, many=True).data
        )


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.select_related(
        "restaurant", "restaurant__owner"
    )
    serializer_class = TableSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TableFilter

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticatedOrReadOnly()]
        return [IsOwner()]