# SKYLINE Flight Management System - Knowledge Base

This document serves as a comprehensive technical overview of the SKYLINE Flight Management application. It is designed to act as a definitive knowledge base for developers or AI assistants working with the codebase.

---

## 1. Technologies Stack

### Backend
*   **Framework:** Django 5.x (Python)
*   **Language:** Python 3
*   **Database:** SQLite3 (`db.sqlite3`)
*   **Authentication:** Django built-in `User` model & Session Authentication.

### Frontend
*   **Markup/Templating:** HTML5 & Django Templates
*   **Styling Framework:** Bootstrap 5.3 (via CDN)
*   **Custom Styling:** CSS3 (Custom Glassmorphism & Light Theme UI)
*   **Iconography:** Bootstrap Icons (via CDN)
*   **Typography:** Google Fonts ('Inter' for UI text, 'Playfair Display' for premium serif headings)
*   **Client-Side Logic:** Vanilla JavaScript (ES6)

---

## 2. Core Data Models (`reservation/models.py`)

The application's business logic relies on two primary custom models, plus the standard Django `User` model.

### `Flight` Model
Represents a scheduled airline flight.
*   `flight_number` (CharField): Airline code + numbers (e.g., "6E915").
*   `origin` / `destination` (CharField): Indian city airports (e.g., "New Delhi (DEL)").
*   `departure_time` / `arrival_time` (DateTimeField): Flight schedule.
*   `total_seats` (PositiveIntegerField): Maximum capacity of the aircraft.
*   `available_seats` (PositiveIntegerField): Real-time tracker of available inventory. Automatically initialized to `total_seats` upon creation.
*   `price` (DecimalField): Base price per single seat in INR (₹).

### `Booking` Model
Associates a registered `User` with a specific `Flight`.
*   `user` (ForeignKey -> User): The customer.
*   `flight` (ForeignKey -> Flight): The booked flight.
*   `seats_booked` (PositiveIntegerField): Number of seats reserved.
*   `total_price` (DecimalField): Total cost (`seats_booked * flight.price`). Auto-calculated overriding the model's `save()` method.
*   `booking_time` (DateTimeField): Timestamp of the transaction.

---

## 3. Application Workflow

### Data Initialization
*   The database is populated using the `seed_flights.py` script. This script deletes existing records and generates randomized domestic Indian flights with realistic constraints (pricing rounded to 100s, departure times offset from current timezone).

### Browsing & Search (Unauthenticated)
1.  **Home Page (`/`)**: Displays a hero section and a limited view of the top 6 available flights.
2.  **All Flights (`/all-flights/`)**: Displays the complete inventory.
3.  **Client-Side Search**: Both pages feature a Vanilla JS search bar that filters the flight cards instantaneously based on matching origin or destination substrings (modifying DOM `display` properties).

### Authentication
*   **Registration (`/register/`)**: Utilizes Django's `UserCreationForm`.
*   **Login (`/login/`)**: Standard authentication. Redirects intelligently using the `?next=` URL parameter if the user was intercepted while trying to book.

### Booking Process (Authenticated)
1.  **Initiation**: User clicks "Book" on a flight card.
2.  **Seat Selection (`/book/<id>/`)**: User inputs the number of seats. Vanilla JS (`updateTotalPrice()`) dynamically calculates and displays the total cost in real-time (`oninput` event) by multiplying the input by the Django-injected `flight.price`.
3.  **Backend Validation**: The `book_flight` view verifies the requested seats do not exceed `flight.available_seats`.
4.  **Transaction**: 
    *   A `Booking` record is created.
    *   `flight.available_seats` is reduced.
    *   User is redirected to the confirmation screen.

### Booking Management (`/bookings/`)
Users can view all their past and active bookings. They have two management controls:
1.  **Partial Cancellation (Reduce Seats)**: Submitting a form to remove `N` seats. The backend reduces `booking.seats_booked`, triggers `.save()` (which recalculates `total_price`), and adds `N` seats back to `flight.available_seats`.
2.  **Full Cancellation**: Deletes the `Booking` record entirely and restores the original booked seat count back to the `Flight` model.

---

## 4. Codebase Directory Structure

```text
c:\Users\divya\Documents\flight_management\SKYLINE\
│
├── seed_flights.py          # Custom script to drop and seed Flight tables.
├── requirements.txt         # Python package dependencies.
├── db.sqlite3               # Main relational database.
│
├── flight_mgmt/             # Django Project Configuration Directory
│   ├── settings.py          # Core settings (Installed apps, database config, auth validators).
│   ├── urls.py              # Root URL routing (Includes reservation.urls).
│   └── wsgi.py / asgi.py    # Deployment entry points.
│
├── reservation/             # Main Application Logic
│   ├── models.py            # ORM definitions (Flight, Booking).
│   ├── views.py             # Controller logic handling requests and returning templates.
│   ├── urls.py              # App-level routing mapping paths to views.
│   ├── forms.py             # Custom Django forms (e.g., UserRegistrationForm).
│   └── migrations/          # Database schema state files.
│
├── templates/               # HTML Presentation Layer
│   ├── base.html            # Core layout wrapper, loads CSS/JS, Navbar, Message alerts.
│   ├── home.html            # Landing page with Top 6 flights & live search.
│   ├── all_flights.html     # Complete flight inventory grid.
│   ├── book_flight.html     # Seat selection form with real-time JS price calculator.
│   ├── flight_detail.html   # Dedicated UI for viewing a single flight's stats.
│   ├── confirm_booking.html # Success screen displaying booking summary.
│   ├── my_bookings.html     # Dashboard displaying user bookings with cancellation controls.
│   ├── login.html           # Authentication UI.
│   └── register.html        # Account creation UI.
│
└── static/                  # Static Assets
    └── css/
        └── styles.css       # Global design system (colors, layout rules, animations).
```

## 5. Notable Architectural Details for LLMs
*   **Security Override**: In `flight_mgmt/settings.py`, the `UserAttributeSimilarityValidator` is currently commented out to allow for simplified local testing (e.g., using passwords similar to the username).
*   **Template Rendering Tricks**: In `book_flight.html`, Django template variables injected into JavaScript are wrapped in `Number("{{ ... }}")` to prevent VS Code/IDE false-positive syntax errors.
*   **State Integrity**: `available_seats` must always be manually updated and saved back to the `Flight` model anytime a `Booking` is created, fully cancelled, or partially reduced.
