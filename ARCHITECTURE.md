# 🏗️ Corner Chair - Architecture Documentation

## System Overview

Corner Chair is a full-stack appointment booking system for barbershops, built with Flask, SQLite, and modern web technologies.

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENT LAYER                         │
│  (HTML/CSS/JavaScript - Browser-Based Interface)        │
├─────────────────────────────────────────────────────────┤
│  - Landing page (barber-demo.html)                      │
│  - Authentication pages (auth.html)                     │
│  - Booking interface (book.html)                        │
│  - Account management pages                            │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/HTTPS
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   SERVER LAYER                          │
│          (Flask Application - Python Backend)           │
├─────────────────────────────────────────────────────────┤
│  app.py - Main Flask application                        │
│  ├── Authentication Routes                             │
│  │   ├── /login - User login                          │
│  │   ├── /register - New user registration            │
│  │   └── /logout - User logout                        │
│  ├── Booking Routes                                    │
│  │   ├── /book - Display booking form                 │
│  │   ├── /api/book - Submit booking                   │
│  │   └── /appointments - View user appointments       │
│  ├── Admin Routes                                      │
│  │   └── /admin - Admin dashboard                     │
│  └── Public Routes                                     │
│      ├── / - Homepage                                  │
│      └── /services - Services page                    │
└────────────────────┬────────────────────────────────────┘
                     │ SQL Queries
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  DATA LAYER                             │
│             (SQLite Database)                           │
├─────────────────────────────────────────────────────────┤
│  cornershop.db                                          │
│  ├── users table                                        │
│  │   ├── id (Primary Key)                             │
│  │   ├── username (Unique)                            │
│  │   ├── email (Unique)                               │
│  │   ├── password_hash                                │
│  │   └── created_at                                   │
│  ├── services table                                    │
│  │   ├── id (Primary Key)                             │
│  │   ├── name                                          │
│  │   ├── description                                  │
│  │   ├── price                                        │
│  │   └── duration_minutes                             │
│  └── appointments table                               │
│      ├── id (Primary Key)                             │
│      ├── user_id (Foreign Key → users)                │
│      ├── service_id (Foreign Key → services)          │
│      ├── appointment_date                             │
│      ├── appointment_time                             │
│      ├── status (pending/confirmed/completed)         │
│      └── created_at                                   │
└─────────────────────────────────────────────────────────┘
```

## Component Breakdown

### 1. Frontend Components

**barber-demo.html**
- Landing page
- Service showcase
- Business hours
- Contact information
- Professional design

**templates/base.html**
- Base HTML template
- Navigation bar
- Footer
- Common styling

**templates/auth.html**
- Login form
- Registration form
- Password validation
- Session management

**templates/book.html**
- Service selection
- Date/time picker
- Form validation
- Booking confirmation

### 2. Backend Components

**app.py** - Flask Application
```python
# Core Functionality
- Flask app initialization
- Database connection
- Session management
- Route handlers
- Error handling
- Security middleware
```

**Key Features:**
- User authentication with password hashing
- Session-based authorization
- CSRF protection
- Input validation
- Error handling and logging

### 3. Database Design

**Users Table**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Services Table**
```sql
CREATE TABLE services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    duration_minutes INTEGER NOT NULL
);
```

**Appointments Table**
```sql
CREATE TABLE appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    service_id INTEGER NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (service_id) REFERENCES services(id)
);
```

## Data Flow

### Booking Flow
```
1. User visits /book
   ↓
2. Frontend displays booking form
   ├── Loads available services
   ├── Shows date picker (business hours)
   └── Shows time slots
   ↓
3. User fills form and submits
   ↓
4. Server validates:
   ├── User authentication
   ├── Date/time validity
   ├── Service availability
   └── Appointment not in past
   ↓
5. If valid:
   ├── Insert appointment to database
   ├── Send confirmation email (future feature)
   └── Redirect to success page
   ↓
6. If invalid:
   ├── Show error message
   └── Return to booking form
```

### Authentication Flow
```
1. User visits /register
   ↓
2. Fills registration form
   ├── Username (unique check)
   ├── Email (unique check)
   ├── Password (hashing)
   └── Confirm password
   ↓
3. Server validates:
   ├── Username available
   ├── Email available
   ├── Password strong enough
   └── No SQL injection attempts
   ↓
4. If valid:
   ├── Hash password with PBKDF2
   ├── Store in database
   ├── Create session
   └── Redirect to dashboard
```

## Security Architecture

### Authentication
- **Password Hashing**: PBKDF2 with salt
- **Session Management**: Secure session cookies
- **CSRF Protection**: Token validation on forms

### Data Protection
- **Input Validation**: All user inputs validated
- **SQL Injection Prevention**: Parameterized queries
- **XSS Prevention**: Template escaping

### API Security
- **HTTPS Ready**: Can use SSL/TLS
- **Rate Limiting**: Optional middleware
- **CORS**: Configurable for API access

## File Structure

```
corner-chair/
├── barber-demo.html              # Landing page
├── barber-booking-demo/          # Main application
│   ├── app.py                    # Flask app
│   ├── requirements.txt           # Dependencies
│   ├── cornershop.db             # SQLite database
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth.html
│   │   └── book.html
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── script.js
│   └── tests/
│       ├── test_booking.py
│       └── test_auth.py
├── README.md                     # Documentation
├── CONTRIBUTING.md               # Contribution guide
└── .gitignore
```

## Key Design Patterns

### 1. MVC (Model-View-Controller)
- **Model**: SQLite database tables
- **View**: Jinja2 templates
- **Controller**: Flask routes in app.py

### 2. Session-Based State Management
```python
@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')
    # Show user's appointments
```

### 3. Template Inheritance
```html
<!-- templates/base.html -->
<html>
  <nav>Navigation</nav>
  {% block content %}{% endblock %}
  <footer>Footer</footer>
</html>

<!-- templates/book.html -->
{% extends "base.html" %}
{% block content %}
  <!-- Booking form -->
{% endblock %}
```

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python 3.8+, Flask |
| Database | SQLite |
| Templates | Jinja2 |
| Security | PBKDF2 (password), CSRF tokens |
| Testing | pytest, unittest |
| Version Control | Git, GitHub |

## Performance Considerations

### Database
- Indexes on frequently queried columns
- Connection pooling ready
- Query optimization

### Caching
- Static file caching (CSS, JS)
- Template caching
- Session-based user data

### Scalability
- Can migrate to PostgreSQL
- Ready for Redis session storage
- Modular design for microservices

## Testing Architecture

```
tests/
├── test_booking.py
│   ├── test_create_appointment()
│   ├── test_invalid_date()
│   ├── test_service_selection()
│   └── test_appointment_conflict()
└── test_auth.py (future)
    ├── test_user_registration()
    ├── test_user_login()
    └── test_session_management()
```

**Test Coverage:**
- Unit tests: Individual functions
- Integration tests: Full flows
- Edge cases: Invalid inputs, boundary conditions

## Future Architecture Enhancements

### Phase 2
- Add email notifications
- Implement calendar view
- Add payment processing
- Admin dashboard enhancements

### Phase 3
- Mobile app (React Native)
- Real-time notifications (WebSockets)
- Advanced scheduling (availability management)
- Multi-location support

### Phase 4
- Machine learning (appointment predictions)
- Analytics dashboard
- CRM integration
- API gateway for third-party integrations

## Deployment Architecture

### Current (Local Development)
```
Developer Machine
  → Flask dev server (127.0.0.1:5001)
  → SQLite database (local file)
```

### Production (Future)
```
GitHub Repository
  ↓ (Deployment trigger)
Heroku/AWS/DigitalOcean
  ├── Flask application (gunicorn)
  ├── PostgreSQL database
  ├── Redis cache
  ├── SSL/TLS
  └── CDN (for static files)
```

## Error Handling Strategy

```python
# Try-except for critical operations
try:
    appointment = create_appointment(data)
    db.session.commit()
except ValueError as e:
    # Return validation error (400)
except DatabaseError as e:
    # Return server error (500)
    log_error(e)
```

## Monitoring & Logging

```python
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Log important events
logging.info(f"User {user_id} booked appointment {app_id}")
logging.error(f"Database connection failed: {error}")
```

---

**Last Updated:** November 14, 2026  
**Version:** 1.0.0  
**Status:** Production Ready

