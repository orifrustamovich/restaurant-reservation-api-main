from tests.factories import RestaurantFactory


class TestRestaurantList:
    def test_list_unauthenticated(self, api_client, db):
        """Autentifikatsiyasiz restoran ro'yxatini ko'rish"""
        RestaurantFactory.create_batch(3)
        response = api_client.get("/api/restaurants/")
        assert response.status_code == 200

    def test_list_returns_active_only(self, api_client, db):
        """Faqat aktiv restoranlar qaytishi"""
        RestaurantFactory(is_active=True)
        RestaurantFactory(is_active=False)
        response = api_client.get("/api/restaurants/")
        assert response.status_code == 200
        results = response.data.get("results", response.data)
        assert len(results) == 1


class TestRestaurantCreate:
    def test_owner_can_create(self, owner_client, owner, db):
        """Owner restoran yarata oladi"""
        data = {
            "name": "Test Restaurant",
            "address": "Seoul",
            "phone": "010-1234-5678",
            "opening_time": "09:00",
            "closing_time": "22:00",
        }
        response = owner_client.post("/api/restaurants/", data)
        assert response.status_code == 201
        assert response.data["name"] == "Test Restaurant"

    def test_customer_cannot_create(self, auth_client, db):
        """Customer restoran yarata olmaydi"""
        data = {
            "name": "Test Restaurant",
            "address": "Seoul",
            "phone": "010-1234-5678",
            "opening_time": "09:00",
            "closing_time": "22:00",
        }
        response = auth_client.post("/api/restaurants/", data)
        assert response.status_code == 403

    def test_unauthenticated_cannot_create(self, api_client, db):
        """Autentifikatsiyasiz yarata olmaydi"""
        response = api_client.post("/api/restaurants/", {})
        assert response.status_code == 401
