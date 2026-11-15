import sqlite3
import tempfile
import unittest
from contextlib import closing
from datetime import date, timedelta
from pathlib import Path

from app import create_app


class BookingTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.database = str(Path(self.directory.name) / "test.sqlite3")
        self.app = create_app({"TESTING": True, "DATABASE": self.database})
        self.client = self.app.test_client()
        self.future_tuesday = date.today() + timedelta(days=(1 - date.today().weekday()) % 7 or 7)

    def post(self, client, url, data):
        client.get(url)
        with client.session_transaction() as session:
            data["csrf_token"] = session["csrf_token"]
        return client.post(url, data=data, follow_redirects=True)

    def register_and_login(self, client, username):
        password = "test-password-123"
        self.post(client, "/register", {
            "username": username, "password": password, "confirm_password": password,
        })
        return self.post(client, "/login", {"username": username, "password": password})

    def appointment(self, **overrides):
        data = {
            "service": "classic",
            "date": self.future_tuesday.isoformat(),
            "time": "09:00",
            "payment": "Apple Pay",
        }
        data.update(overrides)
        return data

    def test_account_and_simulated_booking(self):
        response = self.register_and_login(self.client, "tester")
        self.assertIn(b"Find your next look", response.data)
        response = self.post(self.client, "/book", self.appointment())
        self.assertIn(b"Test appointment saved. No payment was taken.", response.data)
        self.assertIn(b"Apple Pay simulation", response.data)
        with closing(sqlite3.connect(self.database)) as db:
            password_hash = db.execute("SELECT password_hash FROM users").fetchone()[0]
            row = db.execute("SELECT service, price, payment_method FROM appointments").fetchone()
        self.assertNotEqual(password_hash, "test-password-123")
        self.assertEqual(row, ("Classic haircut", 30, "Apple Pay"))

    def test_login_and_csrf_protect_booking(self):
        self.assertEqual(self.client.get("/book").status_code, 302)
        self.assertEqual(self.client.post("/register", data={}).status_code, 400)
        self.register_and_login(self.client, "tester")
        self.assertEqual(self.client.post("/book", data=self.appointment()).status_code, 400)
        with closing(sqlite3.connect(self.database)) as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM appointments").fetchone()[0], 0)

    def test_bad_password_and_duplicate_username(self):
        self.register_and_login(self.client, "tester")
        self.post(self.client, "/logout", {})
        response = self.post(self.client, "/login", {"username": "tester", "password": "wrong"})
        self.assertIn(b"Username or password is incorrect", response.data)
        response = self.post(self.client, "/register", {
            "username": "TESTER", "password": "test-password-123",
            "confirm_password": "test-password-123",
        })
        self.assertIn(b"already in use", response.data)

    def test_invalid_times_and_payment_rejected(self):
        self.register_and_login(self.client, "tester")
        saturday = self.future_tuesday + timedelta(days=4)
        sunday = saturday + timedelta(days=1)
        for values in (
            {"date": sunday.isoformat()},
            {"date": saturday.isoformat(), "time": "17:00"},
            {"date": "invalid"},
            {"payment": "real card"},
            {"service": "unknown"},
            {"date": (date.today() - timedelta(days=1)).isoformat()},
        ):
            response = self.post(self.client, "/book", self.appointment(**values))
            self.assertIn(b'class="flash error"', response.data)
        with closing(sqlite3.connect(self.database)) as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM appointments").fetchone()[0], 0)

    def test_bookings_are_private_and_slots_cannot_be_double_booked(self):
        self.register_and_login(self.client, "first")
        self.post(self.client, "/book", self.appointment())
        second = self.app.test_client()
        self.register_and_login(second, "second")
        response = second.get("/book")
        self.assertNotIn(b"Apple Pay simulation", response.data)
        response = self.post(second, "/book", self.appointment())
        self.assertIn(b"already booked", response.data)
        with closing(sqlite3.connect(self.database)) as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM appointments").fetchone()[0], 1)


if __name__ == "__main__":
    unittest.main()
