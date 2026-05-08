from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import RegisterView, LoginView, LogoutView, ProfileView
from restaurants.views import RestaurantViewSet, TableViewSet
from reservations.views import ReservationViewSet

router = DefaultRouter()
router.register("restaurants", RestaurantViewSet, basename="restaurant")
router.register("tables", TableViewSet, basename="table")
router.register("reservations", ReservationViewSet, basename="reservation")

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/profile/", ProfileView.as_view(), name="profile"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]