import datetime

import factory
from factory.django import DjangoModelFactory

from reservations.models import Reservation
from restaurants.models import Restaurant, Table
from users.models import CustomUser


class UserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser

    email = factory.Sequence(lambda n: f"user{n}@test.com")
    username = factory.Sequence(lambda n: f"user{n}")
    password = factory.PostGenerationMethodCall("set_password", "testpass123")
    role = "customer"


class OwnerFactory(UserFactory):
    role = "owner"
    email = factory.Sequence(lambda n: f"owner{n}@test.com")
    username = factory.Sequence(lambda n: f"owner{n}")


class RestaurantFactory(DjangoModelFactory):
    class Meta:
        model = Restaurant

    owner = factory.SubFactory(OwnerFactory)
    name = factory.Sequence(lambda n: f"Restaurant {n}")
    address = "Seoul, Korea"
    phone = "010-1234-5678"
    opening_time = datetime.time(9, 0)
    closing_time = datetime.time(22, 0)


class TableFactory(DjangoModelFactory):
    class Meta:
        model = Table

    restaurant = factory.SubFactory(RestaurantFactory)
    table_number = factory.Sequence(lambda n: n + 1)
    capacity = 4


class ReservationFactory(DjangoModelFactory):
    class Meta:
        model = Reservation

    customer = factory.SubFactory(UserFactory)
    table = factory.SubFactory(TableFactory)
    reservation_date = factory.LazyFunction(
        lambda: datetime.date.today() + datetime.timedelta(days=1)
    )
    start_time = datetime.time(12, 0)
    end_time = datetime.time(13, 0)
    party_size = 2
