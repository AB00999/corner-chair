import re
import secrets
import sqlite3
from contextlib import closing
from datetime import date, datetime
from functools import wraps
from pathlib import Path

from flask import Flask, abort, flash, redirect, render_template, request, send_file, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

SERVICES = {
    "classic": ("Classic haircut", 30),
    "haircut-beard": ("Haircut & beard", 45),
    "beard": ("Beard trim", 20),
    "kids": ("Kids' haircut", 25),
}
PAYMENT_METHODS = ("Apple Pay", "Cash App", "Tap to Pay", "Zelle")
TIMES = tuple(f"{hour:02}:{minute:02}" for hour in range(9, 18) for minute in (0, 30))
SITE_DIRECTORY = Path(__file__).resolve().parent.parent


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True, static_folder=str(Path(__file__).resolve().parent / "static"))
    app.config.update(
        SECRET_KEY=secrets.token_hex(32),
        DATABASE=str(Path(app.instance_path) / "bookings.sqlite3"),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Strict",
        TRUSTED_HOSTS=["localhost", "127.0.0.1"],
        MAX_CONTENT_LENGTH=16 * 1024,
        TEMPLATES_AUTO_RELOAD=True,
    )
    app.jinja_env.auto_reload = True
    app.jinja_env.cache = None
    if test_config:
        app.config.update(test_config)
    Path(app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)

    def connect():
        connection = sqlite3.connect(app.config["DATABASE"], timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    with closing(connect()) as db, db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE COLLATE NOCASE,
                password_hash TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id),
                service TEXT NOT NULL,
                price INTEGER NOT NULL,
                appointment_date TEXT NOT NULL,
                appointment_time TEXT NOT NULL,
                payment_method TEXT NOT NULL,
                UNIQUE(appointment_date, appointment_time)
            );
            """
        )

    @app.after_request
    def security_headers(response):
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        return response

    @app.before_request
    def check_csrf():
        if request.method == "POST":
            expected = session.get("csrf_token", "")
            supplied = request.form.get("csrf_token", "")
            if not expected or not secrets.compare_digest(expected, supplied):
                abort(400, "The form expired. Reload the page and try again.")

    @app.context_processor
    def template_context():
        if "csrf_token" not in session:
            session["csrf_token"] = secrets.token_urlsafe(32)
        return {"csrf_token": session["csrf_token"]}

    def login_required(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if "user_id" not in session:
                flash("Sign in to book an appointment.", "info")
                return redirect(url_for("login"))
            return view(*args, **kwargs)

        return wrapped

    @app.get("/")
    def home():
        page = (SITE_DIRECTORY / "barber-demo.html").read_text(encoding="utf-8")
        marker = '<a href="#contact">Contact</a>'
        if page.count(marker) != 1:
            raise RuntimeError("The barber navigation could not be found.")
        page = page.replace(marker, marker + '\n                <a href="/book">Book (local test)</a>', 1)
        return page

    @app.get("/services.html")
    def portfolio():
        return send_file(SITE_DIRECTORY / "services.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            if not re.fullmatch(r"[A-Za-z0-9_.-]{3,32}", username):
                flash("Use 3-32 letters, numbers, dots, underscores or hyphens for your username.", "error")
            elif not 12 <= len(password) <= 128:
                flash("Use a test password between 12 and 128 characters.", "error")
            elif password != request.form.get("confirm_password", ""):
                flash("Passwords do not match.", "error")
            else:
                try:
                    with closing(connect()) as db, db:
                        db.execute(
                            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                            (username, generate_password_hash(password)),
                        )
                except sqlite3.IntegrityError:
                    flash("That username is already in use.", "error")
                else:
                    flash("Test account created. Sign in to continue.", "success")
                    return redirect(url_for("login"))
        return render_template("auth.html", register=True)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            with closing(connect()) as db:
                user = db.execute(
                    "SELECT id, username, password_hash FROM users WHERE username = ?", (username,)
                ).fetchone()
            if user is None or not check_password_hash(user["password_hash"], password):
                flash("Username or password is incorrect.", "error")
            else:
                session.clear()
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                return redirect(url_for("book"))
        return render_template("auth.html", register=False)

    @app.post("/logout")
    def logout():
        session.clear()
        flash("You are signed out.", "info")
        return redirect(url_for("home"))

    @app.route("/book", methods=["GET", "POST"])
    @login_required
    def book():
        if request.method == "POST":
            service = request.form.get("service", "")
            day = request.form.get("date", "")
            time = request.form.get("time", "")
            payment = request.form.get("payment", "")
            try:
                chosen_date = date.fromisoformat(day)
            except ValueError:
                chosen_date = None
            now = datetime.now()
            if service not in SERVICES or payment not in PAYMENT_METHODS:
                flash("Choose a listed service and simulated payment method.", "error")
            elif (
                chosen_date is None
                or chosen_date.isoformat() != day
                or chosen_date.weekday() in (0, 6)
                or time not in TIMES
                or (chosen_date.weekday() == 5 and time >= "17:00")
                or datetime.combine(chosen_date, datetime.strptime(time, "%H:%M").time()) <= now
            ):
                flash("Choose a future 30-minute slot during the example opening hours.", "error")
            else:
                name, price = SERVICES[service]
                try:
                    with closing(connect()) as db, db:
                        db.execute(
                            """INSERT INTO appointments
                               (user_id, service, price, appointment_date, appointment_time, payment_method)
                               VALUES (?, ?, ?, ?, ?, ?)""",
                            (session["user_id"], name, price, day, time, payment),
                        )
                except sqlite3.IntegrityError:
                    flash("That time is already booked. Please choose another.", "error")
                else:
                    flash("Test appointment saved. No payment was taken.", "success")
                    return redirect(url_for("book"))
        with closing(connect()) as db:
            appointments = db.execute(
                """SELECT service, price, appointment_date, appointment_time, payment_method
                   FROM appointments WHERE user_id = ?
                   ORDER BY appointment_date, appointment_time""",
                (session["user_id"],),
            ).fetchall()
        return render_template(
            "book.html", services=SERVICES, times=TIMES, payment_methods=PAYMENT_METHODS,
            today=date.today().isoformat(), appointments=appointments,
        )

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5001, debug=False)
