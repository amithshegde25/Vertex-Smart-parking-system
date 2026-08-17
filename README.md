# Smart Parking Management System Using Intelligent Slot Allocation

**Week 3 Software Milestone — Engineering College Project**

---

## 1. Project Title
**Smart Parking Management System Using Intelligent Slot Allocation**

## 2. Problem Statement
Urban and educational campus environments face severe traffic congestion, excessive fuel consumption, and wasted time due to inefficient, unguided parking search. Drivers spend an average of 10–15 minutes searching for available parking spaces due to a lack of real-time spatial visibility and intelligent slot allocation.

## 3. Objectives
- Provide a responsive software-only web platform for real-time digital parking space management.
- Implement an automated **Intelligent Slot Allocation Algorithm** that recommends optimal available slots based on entry proximity.
- Maintain accurate real-time slot statuses (`Available`, `Occupied`, `Reserved`, `Unavailable`) backed by SQLite persistence.
- Demonstrate multidisciplinary engineering concepts (Civil Engineering layout geometry, Mechanical vehicle dimensions, and EEE virtual sensor telemetry).

## 4. Key Features
- **User Authentication**: Secure registration and login with Werkzeug password hashing (`pbkdf2:sha256`) and Flask sessions.
- **Vehicle Information Storage**: Record vehicle registration numbers and classifications (Car, SUV, Two-Wheeler).
- **Digital Parking Layout**: Visual 2D grid representation showing 12 slots (Row A, Row B, Row C) separated by two-way driveway lanes.
- **Intelligent Slot Allocation**: One-click algorithm calculating nearest available entry slot.
- **Atomic Reservation Engine**: Prevents race conditions and duplicate slot reservations; generates unique booking receipts (`SP1001`).
- **Live Telemetry & Statistics**: Real-time counter cards and EEE virtual ultrasonic sensor state monitoring.

## 5. Technology Stack
- **Frontend**: HTML5, Vanilla CSS3 (Custom design system), JavaScript (ES6)
- **Backend**: Python 3.x, Flask Web Framework (`Flask 3.0.2`)
- **Database**: SQLite3 (`parking.db`)
- **Templating**: Jinja2
- **Password Security**: Werkzeug Security (`generate_password_hash`, `check_password_hash`)

## 6. System Architecture

```text
  [ User Browser / Web Interface ]
                │
                ▼ (HTTP Requests / Session Cookie)
     ┌──────────────────────┐
     │  Flask Web Server    │
     │      (app.py)        │
     └──────────┬───────────┘
                │
     ┌──────────┴───────────┐
     │ Allocation Engine &  │
     │  Session Management  │
     └──────────┬───────────┘
                │ (SQL Queries)
                ▼
     ┌──────────────────────┐
     │   SQLite Database    │
     │    (parking.db)      │
     └──────────────────────┘
```

## 7. Database Structure

### `users` Table
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER PRIMARY KEY | Unique user ID |
| `name` | TEXT | User full name |
| `email` | TEXT UNIQUE | Registered email address |
| `password` | TEXT | Hashed password |
| `vehicle_number` | TEXT | Vehicle registration number |
| `vehicle_type` | TEXT | Car / SUV / Two-Wheeler |
| `created_at` | TIMESTAMP | Registration timestamp |

### `parking_slots` Table
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER PRIMARY KEY | Slot ID |
| `slot_number` | TEXT UNIQUE | `A1`..`A4`, `B1`..`B4`, `C1`..`C4` |
| `slot_type` | TEXT | Target vehicle class (`Car`) |
| `status` | TEXT | `Available` / `Occupied` / `Reserved` / `Unavailable` |
| `vehicle_number` | TEXT | Linked vehicle number |

### `bookings` Table
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER PRIMARY KEY | Booking record ID |
| `booking_reference` | TEXT UNIQUE | e.g. `SP1001` |
| `user_id` | INTEGER FK | References `users.id` |
| `slot_id` | INTEGER FK | References `parking_slots.id` |
| `vehicle_number` | TEXT | Vehicle registration |
| `booking_time` | TIMESTAMP | Time reserved |
| `status` | TEXT | `Reserved` / `Active` / `Completed` / `Cancelled` |

## 8. Initial Database Seed (Week 3 Specification)
The system initializes with 12 slots:
- **Available (8)**: A1, A3, A4, B2, B3, C1, C2, C4
- **Occupied (4)**: A2, B1, B4, C3

## 9. How to Install

### Prerequisites
- Python 3.8+ installed on laptop / local system

### Setup Virtual Environment & Dependencies
```bash
# 1. Open terminal inside project folder
cd Smart-Parking-System

# 2. Create Python virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Command Prompt:
.\venv\Scripts\activate.bat
# On macOS/Linux:
source venv/bin/activate

# 4. Install required packages
pip install -r requirements.txt
```

## 10. How to Run

### Step 1: Initialize Database
```bash
python database/init_db.py
```

### Step 2: Launch Flask Server
```bash
python app.py
```

### Step 3: Access Web Application
Open your web browser and navigate to:
```text
http://127.0.0.1:5000/
```

## 11. Project Structure
```text
Smart-Parking-System/
│
├── app.py                  # Main Flask routes, session handling & allocation logic
├── requirements.txt        # Python package dependencies
├── parking.db              # SQLite database file (auto-generated)
├── README.md               # Complete project documentation
│
├── database/
│   └── init_db.py          # Database initialization & seed script
│
├── templates/
│   ├── base.html           # Master layout & navbar template
│   ├── index.html          # Homepage with real-time stats & features
│   ├── login.html          # User authentication page
│   ├── register.html       # Account & vehicle registration page
│   ├── dashboard.html      # Protected user dashboard & allocation trigger
│   ├── parking.html        # Interactive 2D digital layout & sensor telemetry
│   └── booking.html        # Active reservation receipt & cancellation page
│
└── static/
    ├── css/
    │   └── style.css       # Responsive styling, slot cards & badge colors
    └── js/
        └── script.js       # Client validation & UI interaction scripts
```

## 12. Week 3 Scope
- **Included**: Complete software web application, user registration, authentication, database persistence, dynamic statistics calculation, proximity-based Intelligent Slot Allocation, atomic reservation engine, 2D parking layout grid with driveway geometry, and virtual sensor status simulation panel.
- **Excluded**: Hardware sensor wiring, microcontrollers, physical barrier servos, AI computer vision, external payment gateways (planned for future milestone phases).

## 13. Future Scope
- **Week 5 Integration**: ESP32 / Arduino hardware connectivity via MQTT/WebSockets to sync physical ultrasonic sensors in real-time.
- **Computer Vision**: ANPR (Automatic Number Plate Recognition) for automated gate access.
- **Payment Gateway**: Integrated parking fee calculation & digital payment processing.
- **Mobile Application**: Flutter cross-platform mobile client integration.
