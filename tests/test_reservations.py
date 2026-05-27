import datetime

from tests.factories import ReservationFactory, TableFactory


class TestReservationConflict:
    def test_no_conflict_different_time(self, auth_client, db):
        """Har xil vaqtda bron — conflict bo'lmasin"""
        table = TableFactory(capacity=4)
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)

        # Birinchi bron: 12:00-13:00
        ReservationFactory(
            table=table,
            reservation_date=tomorrow,
            start_time=datetime.time(12, 0),
            end_time=datetime.time(13, 0),
        )

        # Ikkinchi bron: 14:00-15:00 — conflict yo'q
        data = {
            "table": table.id,
            "reservation_date": tomorrow.isoformat(),
            "start_time": "14:00",
            "end_time": "15:00",
            "party_size": 2,
        }
        response = auth_client.post("/api/reservations/", data)
        assert response.status_code == 201

    def test_conflict_detected(self, auth_client, db):
        """Bir vaqtda 2 ta bron — conflict chiqishi kerak"""
        table = TableFactory(capacity=4)
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)

        # Birinchi bron: 12:00-14:00
        ReservationFactory(
            table=table,
            reservation_date=tomorrow,
            start_time=datetime.time(12, 0),
            end_time=datetime.time(14, 0),
        )

        # Ikkinchi bron: 13:00-15:00 — kesishadi!
        data = {
            "table": table.id,
            "reservation_date": tomorrow.isoformat(),
            "start_time": "13:00",
            "end_time": "15:00",
            "party_size": 2,
        }
        response = auth_client.post("/api/reservations/", data)
        assert response.status_code == 400

    def test_past_date_rejected(self, auth_client, db):
        """O'tib ketgan sanaga bron — 400"""
        table = TableFactory(capacity=4)
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        data = {
            "table": table.id,
            "reservation_date": yesterday.isoformat(),
            "start_time": "12:00",
            "end_time": "13:00",
            "party_size": 2,
        }
        response = auth_client.post("/api/reservations/", data)
        assert response.status_code == 400

    def test_cancel_past_reservation(self, auth_client, customer, db):
        """O'tib ketgan bronni bekor qilib bo'lmaydi"""
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        reservation = ReservationFactory(
            customer=customer,
            reservation_date=yesterday,
        )
        response = auth_client.post(f"/api/reservations/{reservation.id}/cancel/")
        assert response.status_code == 400

    def test_capacity_exceeded(self, auth_client, db):
        """Stol sig'imidan ko'p kishi — 400"""
        table = TableFactory(capacity=2)
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        data = {
            "table": table.id,
            "reservation_date": tomorrow.isoformat(),
            "start_time": "12:00",
            "end_time": "13:00",
            "party_size": 5,  # capacity=2, bu 5 kishi
        }
        response = auth_client.post("/api/reservations/", data)
        assert response.status_code == 400

    def test_cancel_own_reservation(self, auth_client, customer, db):
        """O'z bronini bekor qilish"""
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        reservation = ReservationFactory(
            customer=customer,
            reservation_date=tomorrow,
        )
        response = auth_client.post(f"/api/reservations/{reservation.id}/cancel/")
        assert response.status_code == 200
