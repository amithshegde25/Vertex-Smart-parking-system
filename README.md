# 🚗 Vertex Smart Parking System

### Smart Parking Management System Using Intelligent Slot Allocation

A full-stack **Smart Parking Management System** developed as an engineering college project to digitally manage parking spaces, provide intelligent slot allocation, support user reservations, and visualize parking availability through an interactive web interface.

The application is built using **Python Flask, SQLite, HTML5, CSS3, JavaScript, and Jinja2** and is deployed as a web application.

---

## 🌐 Live Demo

###  [Vertex Smart Parking System](https://vertex-smart-parking-system.vercel.app/)

---

## 📌 Project Overview

Finding an appropriate parking space in a crowded parking facility can waste time and increase unnecessary vehicle movement.

Traditional parking systems often require drivers to manually search for available spaces. This creates several problems:

* Difficulty identifying available parking slots
* Unnecessary movement inside parking areas
* Increased congestion
* Poor visibility of parking availability
* Manual parking management
* Difficulty maintaining reservation records

**Vertex Smart Parking System** addresses these problems by providing a centralized digital parking-management platform.

The system maintains the status of parking slots and allows registered users to store their vehicle information, view parking availability, receive an intelligently allocated parking slot, and create/manage reservations.

The application also includes a **virtual sensor telemetry interface**, representing how physical parking sensors could eventually be integrated into the system.

---

# 🎯 Objectives

The major objectives of the project are:

* Develop a web-based parking management system.
* Digitally represent the physical parking area.
* Display current parking-slot availability.
* Implement intelligent parking-slot allocation.
* Consider entry proximity when selecting a suitable slot.
* Allow users to register and securely log in.
* Store vehicle registration information.
* Allow users to reserve parking slots.
* Generate unique booking references.
* Maintain persistent parking information using SQLite.
* Provide real-time parking statistics.
* Demonstrate how the software can be extended toward IoT-based smart parking.

---

# ✨ Key Features

## 🔐 1. User Registration & Authentication

Users can create an account by providing:

* Name
* Email
* Password
* Vehicle registration number
* Vehicle type

Supported vehicle classifications include:

* 🚗 Car
* 🚙 SUV
* 🏍️ Two-Wheeler

Passwords are stored using **Werkzeug password hashing** rather than storing plaintext passwords.

The application uses Flask sessions to maintain the logged-in user's state.

---

## 📊 2. Parking Statistics Dashboard

The application dynamically calculates parking statistics from the database.

The dashboard provides information such as:

| Statistic   | Meaning                        |
| ----------- | ------------------------------ |
| Total Slots | Total number of parking spaces |
| Available   | Slots currently available      |
| Occupied    | Slots currently occupied       |
| Reserved    | Slots currently reserved       |
| Unavailable | Slots temporarily unavailable  |

The current system is initialized with **12 parking slots**.

---

## 🅿️ 3. Digital 2D Parking Layout

The parking facility is represented digitally using a 2D layout.

The system contains three rows:

```text
        PARKING AREA

     A1   A2   A3   A4

     B1   B2   B3   B4

     C1   C2   C3   C4
```

The parking layout also represents driveway movement between parking rows.

Each slot has:

* Unique slot number
* Slot type
* Current status
* Associated vehicle information when applicable

---

# 🟢 Parking Slot States

Each parking slot can have one of the following states:

### Available

The slot is currently free and can be considered for allocation.

### Occupied

The slot is currently being used by a vehicle.

### Reserved

The slot has been reserved by a user.

### Unavailable

The slot cannot currently be used.

The system uses these states to maintain an up-to-date representation of the parking facility.

---

# 🧠 4. Intelligent Slot Allocation

The main feature that differentiates this project from a basic parking-booking website is the **Intelligent Slot Allocation Algorithm**.

Instead of simply asking the user to manually choose any parking space, the application can calculate a suitable available slot based on **entry proximity**.

### Allocation concept

```text
              User / Vehicle
                    │
                    ▼
          Check Parking Availability
                    │
                    ▼
           Find Available Slots
                    │
                    ▼
          Evaluate Slot Proximity
                    │
                    ▼
        Select Suitable Parking Slot
                    │
                    ▼
             Reserve Slot
```

The application evaluates available parking spaces and selects an appropriate slot according to the defined allocation logic.

This helps reduce unnecessary searching inside the parking area.

---

# 📍 Proximity-Based Allocation

The parking layout is organized into rows and slots.

The allocation algorithm uses the slot's position relative to the parking entrance to determine which available slot is nearest according to the implemented layout logic.

For example, if multiple slots are available:

```text
A1     A3     A4

B2     B3

C1     C2     C4
```

the allocation logic evaluates their position and selects the appropriate available slot rather than simply relying on arbitrary user selection.

This provides a foundation for more advanced routing and optimization algorithms in future versions.

---

# 📅 5. Parking Reservation

Once a suitable slot is identified, the user can create a parking reservation.

The reservation process can be represented as:

```text
User Login
    │
    ▼
View Parking Information
    │
    ▼
Request Slot Allocation
    │
    ▼
Check Slot Availability
    │
    ▼
Select Suitable Slot
    │
    ▼
Create Booking
    │
    ▼
Generate Booking Reference
    │
    ▼
Update Slot Status
```

---

# 🎫 6. Unique Booking Reference

Each booking receives a unique booking reference.

Example:

```text
SP1001
```

The reference can be used to identify the user's reservation.

The booking record stores information such as:

* Booking ID
* Booking reference
* User
* Parking slot
* Vehicle number
* Booking time
* Booking status

---

# 🔄 7. Booking Status Management

Bookings can have different states:

```text
Reserved
   │
   ▼
Active
   │
   ▼
Completed
```

A reservation can also be:

```text
Reserved
   │
   ▼
Cancelled
```

This allows the system to maintain the lifecycle of a parking reservation.

---

# 📡 8. Virtual Sensor Telemetry

The project also includes a **virtual sensor telemetry interface**.

This represents how physical sensors could communicate parking-slot information to the software system.

The current implementation is software-based and does **not** require physical sensors.

The concept can be represented as:

```text
Parking Sensor
      │
      ▼
Vehicle Detection
      │
      ▼
Parking Status
      │
      ▼
Backend
      │
      ▼
SQLite Database
      │
      ▼
Web Dashboard
```

This creates a foundation for future hardware integration using technologies such as ESP32, Arduino, MQTT, or WebSockets.

---

# 🏗️ System Architecture

The current system follows a simple web-application architecture:

```text
                  ┌─────────────────────┐
                  │       USER          │
                  │   Web Browser       │
                  └──────────┬──────────┘
                             │
                             │ HTTP Requests
                             ▼
                  ┌─────────────────────┐
                  │    FLASK SERVER     │
                  │      app.py         │
                  └──────────┬──────────┘
                             │
             ┌───────────────┼────────────────┐
             │               │                │
             ▼               ▼                ▼
       Authentication   Slot Allocation   Reservations
             │               │                │
             └───────────────┼────────────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │   SQLite Database   │
                  │     parking.db      │
                  └─────────────────────┘
```

---

# 🛠️ Technology Stack

## Frontend

### HTML5

Used for:

* Page structure
* Forms
* Dashboard
* Parking layout
* Booking interface

### CSS3

Used for:

* Responsive layout
* Parking-slot visualization
* Cards
* Navigation
* Status indicators
* Overall application styling

### JavaScript ES6

Used for:

* Client-side interactions
* Form validation
* Dynamic UI behavior

---

## Backend

### Python

Python is used for the server-side application logic.

### Flask

Flask handles:

* HTTP requests
* Routing
* Authentication
* Sessions
* Database interaction
* Rendering HTML templates
* Parking allocation
* Reservation processing

The main backend application is contained in:

```text
app.py
```

---

## Template Engine

### Jinja2

Jinja2 is used to dynamically render data from the Flask backend into HTML templates.

For example, parking statistics retrieved from the database can be passed from Flask to the corresponding HTML page.

---

## Database

### SQLite3

SQLite is used as the persistent database.

The database stores:

* User information
* Vehicle information
* Parking-slot information
* Booking information

SQLite is suitable for this project because it is lightweight, file-based, and easy to integrate with Flask.

---

## Security

### Werkzeug Security

Werkzeug provides password hashing and password verification.

The application uses:

```python
generate_password_hash()
```

for storing passwords securely and:

```python
check_password_hash()
```

for verifying login credentials.

---

# 🗄️ Database Design

The application uses three primary database tables.

---

## `users`

Stores registered users and their vehicle information.

| Field            | Type      | Description                 |
| ---------------- | --------- | --------------------------- |
| `id`             | INTEGER   | Unique user ID              |
| `name`           | TEXT      | User's name                 |
| `email`          | TEXT      | Unique email address        |
| `password`       | TEXT      | Hashed password             |
| `vehicle_number` | TEXT      | Vehicle registration number |
| `vehicle_type`   | TEXT      | Car / SUV / Two-Wheeler     |
| `created_at`     | TIMESTAMP | Registration time           |

---

## `parking_slots`

Stores information about individual parking spaces.

| Field            | Type    | Description                |
| ---------------- | ------- | -------------------------- |
| `id`             | INTEGER | Unique slot ID             |
| `slot_number`    | TEXT    | Parking identifier         |
| `slot_type`      | TEXT    | Vehicle category supported |
| `status`         | TEXT    | Current slot status        |
| `vehicle_number` | TEXT    | Associated vehicle number  |

The current parking layout contains:

```text
A1 A2 A3 A4
B1 B2 B3 B4
C1 C2 C3 C4
```

---

## `bookings`

Stores reservation information.

| Field               | Type      | Description              |
| ------------------- | --------- | ------------------------ |
| `id`                | INTEGER   | Booking ID               |
| `booking_reference` | TEXT      | Unique booking reference |
| `user_id`           | INTEGER   | Associated user          |
| `slot_id`           | INTEGER   | Reserved slot            |
| `vehicle_number`    | TEXT      | Vehicle registration     |
| `booking_time`      | TIMESTAMP | Reservation time         |
| `status`            | TEXT      | Booking state            |

---

# 🔗 Database Relationships

The relationship between the tables can be represented as:

```text
┌──────────────┐
│    USERS     │
└──────┬───────┘
       │
       │ user_id
       ▼
┌──────────────┐
│   BOOKINGS   │
└──────┬───────┘
       │
       │ slot_id
       ▼
┌──────────────┐
│ PARKING_SLOTS│
└──────────────┘
```

A booking connects a user to a particular parking slot.

---

# 📁 Project Structure

```text
Vertex-Smart-parking-system/
│
├── app.py
│
├── database/
│   └── init_db.py
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       └── script.js
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── parking.html
│   └── booking.html
│
├── requirements.txt
├── vercel.json
├── .gitignore
└── README.md
```

---

# 🔄 Complete Application Flow

```text
                    START
                      │
                      ▼
               Open Website
                      │
                      ▼
            ┌──────────────────┐
            │ Register / Login │
            └────────┬─────────┘
                     │
                     ▼
                Dashboard
                     │
           ┌─────────┴─────────┐
           │                   │
           ▼                   ▼
    View Statistics      Request Parking
                               │
                               ▼
                     Check Available Slots
                               │
                               ▼
                     Intelligent Allocation
                               │
                               ▼
                       Select Suitable Slot
                               │
                               ▼
                         Create Booking
                               │
                               ▼
                    Generate Booking Reference
                               │
                               ▼
                       Update Slot Status
                               │
                               ▼
                       Booking Confirmation
                               │
                               ▼
                              END
```

---

# 🧪 Initial Parking Configuration

The application initializes with **12 parking slots**.

### Available Slots

```text
A1
A3
A4
B2
B3
C1
C2
C4
```

### Occupied Slots

```text
A2
B1
B4
C3
```

Therefore:

```text
Total Slots     = 12
Available       = 8
Occupied        = 4
Reserved        = 0
```

The actual status can change as reservations and parking operations occur.

---

# 🚀 Installation

## Prerequisites

Make sure the following are installed:

* Python 3.8 or higher
* Git
* A modern web browser

---

## 1. Clone the Repository

```bash
git clone https://github.com/amithshegde25/Vertex-Smart-parking-system.git
```

Navigate into the project:

```bash
cd Vertex-Smart-parking-system
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Initialize the Database

Run:

```bash
python database/init_db.py
```

This initializes the SQLite database and creates the required tables and initial parking-slot data.

---

## 5. Start the Flask Application

```bash
python app.py
```

The application will start on the local Flask development server.

Open:

```text
http://127.0.0.1:5000/
```

in your browser.

---

# ☁️ Deployment

The application includes a `vercel.json` configuration file for deployment through Vercel.

The deployed application is available at:

```text
https://vertex-smart-parking-system.vercel.app/
```

For production deployment, environment-specific configuration such as the Flask secret key should be managed using deployment environment variables rather than storing secrets directly in source code.

---

# 🧪 Example User Journey

A typical user interaction looks like this:

### 1. Registration

The user creates an account and enters:

```text
Name
Email
Password
Vehicle Number
Vehicle Type
```

### 2. Login

The user logs into the application.

### 3. Dashboard

The system displays the user's information and current parking statistics.

### 4. Parking Allocation

The user requests parking allocation.

The system checks available slots and uses the implemented proximity-based allocation logic.

### 5. Reservation

The selected slot is reserved.

### 6. Booking Reference

A unique booking reference is generated.

### 7. Parking Status

The slot's state is updated accordingly.

---

# 🔐 Authentication Flow

The authentication process works as follows:

```text
Registration
     │
     ▼
Validate User Input
     │
     ▼
Hash Password
     │
     ▼
Store User in SQLite
     │
     ▼
Login
     │
     ▼
Retrieve User
     │
     ▼
Verify Password Hash
     │
     ▼
Create Flask Session
     │
     ▼
Access Protected Dashboard
```

Protected routes use a login-check mechanism to prevent unauthenticated users from accessing user-specific pages.

---

# 🧮 Parking Statistics

Parking statistics are calculated from the current database state.

The backend groups parking slots by their status and calculates counts for:

```text
Available
Occupied
Reserved
Unavailable
```

This means the dashboard is not simply displaying hard-coded numbers; it can derive the current state from the parking database.

---

# 🧩 Multidisciplinary Engineering Concept

The project demonstrates concepts from multiple engineering disciplines.

## 💻 Computer Science

* Web development
* Database management
* Authentication
* Backend programming
* Algorithms
* User-interface design

## 🏗️ Civil Engineering

* Parking layout
* Slot geometry
* Driveway arrangement
* Space utilization
* Vehicle circulation

## ⚙️ Mechanical Engineering

* Vehicle classifications
* Vehicle dimensions
* Parking-space requirements
* Vehicle maneuverability

## ⚡ Electrical & Electronics Engineering

The current project uses **virtual sensor telemetry** as a software representation.

The architecture can later be connected to:

* Ultrasonic sensors
* ESP32
* Arduino
* IoT communication
* Real-time occupancy detection

---

# ⚠️ Current Scope & Limitations

This version focuses primarily on the **software implementation** of the smart parking system.

### Currently Included

* Web application
* User registration
* User authentication
* SQLite persistence
* Vehicle information
* Parking statistics
* Intelligent slot allocation
* Parking reservation
* Booking references
* 2D parking layout
* Virtual sensor telemetry

### Not Yet Included

* Physical ultrasonic sensors
* Physical microcontrollers
* Automatic gate/barrier hardware
* Computer-vision-based vehicle detection
* Automatic number plate recognition
* External payment gateway

These are potential extensions for future development.

---

# 🔮 Future Scope

## 1. IoT Sensor Integration

Physical sensors can detect whether a vehicle is occupying a slot.

Possible architecture:

```text
Ultrasonic Sensor
       │
       ▼
ESP32 / Arduino
       │
       ▼
MQTT / WebSocket
       │
       ▼
Flask Backend
       │
       ▼
SQLite / Cloud Database
       │
       ▼
Web Dashboard
```

---

## 2. Automatic Number Plate Recognition

ANPR can automatically identify vehicles entering and leaving the parking facility.

```text
Vehicle
   ↓
Camera
   ↓
Number Plate Detection
   ↓
Vehicle Identification
   ↓
Reservation Verification
   ↓
Entry / Exit
```

---

## 3. Online Payment

Future versions can include:

* Parking fee calculation
* Online payments
* Digital receipts
* Payment history

---

## 4. Mobile Application

A Flutter or native mobile application could provide:

* Parking search
* Slot reservation
* Booking history
* Notifications
* Navigation
* Payment

---

## 5. Smart Navigation

The system could guide users from the parking entrance to their assigned slot.

This would be particularly useful for large parking facilities such as:

* Shopping malls
* Airports
* Universities
* Hospitals
* Stadiums

---

## 6. Data Analytics

Historical parking data could be analyzed to identify:

* Peak parking hours
* Average parking duration
* High-demand slots
* Occupancy trends

This could help parking operators improve space utilization.

---

# 📈 Possible Future Architecture

```text
                       ┌───────────────┐
                       │   Web Client  │
                       └───────┬───────┘
                               │
                       ┌───────▼───────┐
                       │ Mobile Client │
                       └───────┬───────┘
                               │
                               ▼
                    ┌────────────────────┐
                    │   Flask Backend    │
                    │      / API         │
                    └─────────┬──────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
      Database           Allocation          Payment
                            Engine             System
          │
          │
          ▼
     IoT Integration
          │
     ┌────┴────┐
     ▼         ▼
  Sensors   Cameras
     │         │
     └────┬────┘
          ▼
   Real-Time Parking
      Information
```

---

# 🏢 Potential Applications

The system can be adapted for:

* 🎓 Colleges and universities
* 🏢 Corporate offices
* 🏥 Hospitals
* 🏬 Shopping malls
* 🏨 Hotels
* ✈️ Airports
* 🚉 Railway stations
* 🏟️ Stadiums
* 🏘️ Residential communities
* 🏙️ Smart-city parking facilities

---

# ⭐ Project Highlights

* 🅿️ Digital parking management
* 🧠 Intelligent proximity-based slot allocation
* 🔐 User authentication
* 🚗 Vehicle information management
* 📊 Dynamic parking statistics
* 📅 Reservation system
* 🎫 Unique booking references
* 🗄️ SQLite persistence
* 📡 Virtual sensor telemetry
* 🗺️ Interactive 2D parking layout
* 🌐 Web-based architecture
* ☁️ Vercel deployment
* 🔮 Expandable toward IoT and smart-city applications

---

# 🛡️ Security Notes

The application uses password hashing through Werkzeug rather than storing plaintext passwords.

For a production deployment, additional security improvements should be implemented, including:

* Store Flask `SECRET_KEY` in environment variables
* Strong password policies
* CSRF protection
* Secure session configuration
* Input validation
* Rate limiting
* HTTPS-only cookies
* Secure database configuration
* Production-grade server configuration

**Never commit real passwords, API keys, tokens, or other secrets to GitHub.**

---

# 🤝 Contributing

Contributions and improvements are welcome.

A typical contribution workflow is:

```bash
git checkout -b feature/new-feature
```

Make your changes, test them, then:

```bash
git add .
git commit -m "Add new feature"
git push origin feature/new-feature
```

Create a Pull Request on GitHub.

---

# 📜 License

This project was developed as an **engineering college project**.

If the project is intended for open-source distribution, an explicit license such as MIT can be added to the repository.

---

# 👨‍💻 Project

**Vertex Smart Parking System**

**Project Type:** Engineering College Project
**Domain:** Smart Parking / Web Application / Intelligent Slot Allocation
**Backend:** Python + Flask
**Database:** SQLite
**Frontend:** HTML5 + CSS3 + JavaScript
**Deployment:** Vercel

---

## 📌 Summary

**Vertex Smart Parking System** is a web-based parking-management platform that combines digital parking visualization, database-backed slot management, intelligent proximity-based slot allocation, user authentication, and parking reservations.

The current software implementation provides the foundation for a larger smart-parking ecosystem. Future integration with IoT sensors, automatic number plate recognition, online payments, mobile applications, and real-time analytics can further extend the system into a complete smart parking solution.
