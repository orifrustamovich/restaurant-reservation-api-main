from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from reservations.views import ReservationViewSet
from restaurants.views import RestaurantViewSet, TableViewSet
from users.views import LoginView, LogoutView, ProfileView, RegisterView

# Router — ViewSet'larni avtomatik URL'larga bog'laydi
router = DefaultRouter()
router.register("restaurants", RestaurantViewSet, basename="restaurant")
router.register("tables", TableViewSet, basename="table")
router.register("reservations", ReservationViewSet, basename="reservation")

urlpatterns = [
    # Auth endpoints
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/profile/", ProfileView.as_view(), name="profile"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Router bilan yaratilgan URLlar:
    # GET  /api/restaurants/
    # POST /api/restaurants/
    # GET  /api/restaurants/{id}/
    # PUT  /api/restaurants/{id}/
    # ...
    path("", include(router.urls)),
]
