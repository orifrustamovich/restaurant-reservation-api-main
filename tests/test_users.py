import pytest
from tests.factories import UserFactory


class TestRegister:
    def test_register_customer_success(self, api_client, db):
        """Customer muvaffaqiyatli ro'yxatdan o'tishi"""
        data = {
            "email": "new@test.com",
            "username": "newuser",
            "password": "testpass123",
            "password2": "testpass123",
            "role": "customer",
        }
        response = api_client.post("/api/auth/register/", data)
        assert response.status_code == 201
        assert "access" in response.data
        assert "refresh" in response.data
        assert response.data["user"]["email"] == "new@test.com"

    def test_register_password_mismatch(self, api_client, db):
        """Parollar mos kelmasligi — 400 qaytishi kerak"""
        data = {
            "email": "new@test.com",
            "username": "newuser",
            "password": "testpass123",
            "password2": "wrongpass",
            "role": "customer",
        }
        response = api_client.post("/api/auth/register/", data)
        assert response.status_code == 400

    def test_register_duplicate_email(self, api_client, db):
        """Bir xil email bilan ikki marta — 400 qaytishi kerak"""
        UserFactory(email="exist@test.com")
        data = {
            "email": "exist@test.com",
            "username": "newuser",
            "password": "testpass123",
            "password2": "testpass123",
            "role": "customer",
        }
        response = api_client.post("/api/auth/register/", data)
        assert response.status_code == 400

    def test_register_owner_success(self, api_client, db):
        """Owner ro'yxatdan o'tishi"""
        data = {
            "email": "owner@test.com",
            "username": "owneruser",
            "password": "testpass123",
            "password2": "testpass123",
            "role": "owner",
        }
        response = api_client.post("/api/auth/register/", data)
        assert response.status_code == 201
        assert response.data["user"]["role"] == "owner"


class TestLogin:
    def test_login_success(self, api_client, db):
        """Muvaffaqiyatli login"""
        user = UserFactory(email="test@test.com")
        user.set_password("testpass123")
        user.save()
        response = api_client.post(
            "/api/auth/login/",
            {"email": "test@test.com", "password": "testpass123"},
        )
        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_wrong_password(self, api_client, db):
        """Noto'g'ri parol — 400 qaytishi kerak"""
        UserFactory(email="test@test.com")
        response = api_client.post(
            "/api/auth/login/",
            {"email": "test@test.com", "password": "wrongpass"},
        )
        assert response.status_code == 400

    def test_login_nonexistent_email(self, api_client, db):
        """Mavjud bo'lmagan email"""
        response = api_client.post(
            "/api/auth/login/",
            {"email": "noone@test.com", "password": "testpass123"},
        )
        assert response.status_code == 400


class TestProfile:
    def test_profile_authenticated(self, auth_client, customer):
        """Autentifikatsiya qilingan user profilini ko'rishi"""
        response = auth_client.get("/api/auth/profile/")
        assert response.status_code == 200
        assert response.data["email"] == customer.email

    def test_profile_unauthenticated(self, api_client):
        """Autentifikatsiya qilinmagan — 401"""
        response = api_client.get("/api/auth/profile/")
        assert response.status_code == 401