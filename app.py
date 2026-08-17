import os
import sqlite3
from functools import wraps
from flask import (
    Flask, render_template, request, redirect, url_for, flash, session, g
)
from werkzeug.security import generate_password_hash, check_password_hash
from database.init_db import init_db, get_db_path

app = Flask(__name__)
app.secret_key = 'smart_parking_secret_key_week3_milestone'

# Ensure DB initialized on server start
with app.app_context():
    init_db()

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(get_db_path())
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Authentication Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Helper to fetch parking stats from DB
def fetch_parking_stats():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT status, COUNT(*) as count FROM parking_slots GROUP BY status")
    rows = cursor.fetchall()
    
    stats = {'total': 12, 'available': 0, 'occupied': 0, 'reserved': 0, 'unavailable': 0}
    for row in rows:
        status_key = row['status'].lower()
        if status_key in stats:
            stats[status_key] = row['count']
            
    cursor.execute("SELECT COUNT(*) FROM parking_slots")
    total_count = cursor.fetchone()[0]
    if total_count > 0:
        stats['total'] = total_count
        
    return stats

# Helper to fetch user's active booking
def get_user_active_booking(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT b.id, b.booking_reference, b.booking_time, b.status, b.vehicle_number,
               p.slot_number, p.slot_type, u.name as user_name, u.email as user_email
        FROM bookings b
        JOIN parking_slots p ON b.slot_id = p.id
        JOIN users u ON b.user_id = u.id
        WHERE b.user_id = ? AND b.status = 'Reserved'
        ORDER BY b.id DESC LIMIT 1
    ''', (user_id,))
    return cursor.fetchone()

# Route: Homepage
@app.route('/')
def index():
    stats = fetch_parking_stats()
    return render_template(
        'index.html',
        total_slots=stats['total'],
        available_slots=stats['available'],
        occupied_slots=stats['occupied'],
        reserved_slots=stats['reserved']
    )

# Route: Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        vehicle_number = request.form.get('vehicle_number', '').strip().upper()
        vehicle_type = request.form.get('vehicle_type', 'Car')

        # Validation
        if not name or not email or not password or not vehicle_number:
            flash('All required fields must be completed.', 'danger')
            return render_template('register.html')

        if '@' not in email or '.' not in email:
            flash('Please enter a valid email address.', 'danger')
            return render_template('register.html')

        if password != confirm_password:
            flash('Password and confirm password must match.', 'danger')
            return render_template('register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('register.html')

        db = get_db()
        cursor = db.cursor()
        
        # Check if email exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            flash('Email address is already registered. Please log in.', 'danger')
            return render_template('register.html')

        # Store user with Werkzeug password hashing
        password_hash = generate_password_hash(password)
        try:
            cursor.execute('''
                INSERT INTO users (name, email, password, vehicle_number, vehicle_type)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, email, password_hash, vehicle_number, vehicle_type))
            db.commit()

            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.Error as e:
            flash('An error occurred during registration. Please try again.', 'danger')
            return render_template('register.html')

    return render_template('register.html')

# Route: Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Please enter both email and password.', 'danger')
            return render_template('login.html')

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_email'] = user['email']
            session['vehicle_number'] = user['vehicle_number']
            session['vehicle_type'] = user['vehicle_type']

            flash(f"Welcome back, {user['name']}!", 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('login.html')

# Route: Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

# Route: Protected User Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    stats = fetch_parking_stats()
    active_booking = get_user_active_booking(session['user_id'])
    
    user_info = {
        'name': session.get('user_name'),
        'email': session.get('user_email'),
        'vehicle_number': session.get('vehicle_number'),
        'vehicle_type': session.get('vehicle_type')
    }

    return render_template(
        'dashboard.html',
        user=user_info,
        stats=stats,
        active_booking=active_booking,
        recommended_slot=None
    )

# Route: Intelligent Slot Allocation Algorithm
@app.route('/find-parking', methods=['POST'])
@login_required
def find_parking():
    db = get_db()
    cursor = db.cursor()

    # Query all available slots, ordered by entry proximity (Row A > Row B > Row C)
    cursor.execute('''
        SELECT * FROM parking_slots 
        WHERE status = 'Available'
        ORDER BY slot_number ASC
    ''')
    available_slots = cursor.fetchall()

    stats = fetch_parking_stats()
    active_booking = get_user_active_booking(session['user_id'])
    user_info = {
        'name': session.get('user_name'),
        'email': session.get('user_email'),
        'vehicle_number': session.get('vehicle_number'),
        'vehicle_type': session.get('vehicle_type')
    }

    if available_slots:
        # Intelligent allocation selects the first optimal available slot closest to entry
        recommended = available_slots[0]
        flash(f"Intelligent Allocation Engine recommended Slot {recommended['slot_number']} based on proximity.", 'info')
        return render_template(
            'dashboard.html',
            user=user_info,
            stats=stats,
            active_booking=active_booking,
            recommended_slot=recommended
        )
    else:
        flash("No parking slots are currently available.", 'warning')
        return render_template(
            'dashboard.html',
            user=user_info,
            stats=stats,
            active_booking=active_booking,
            recommended_slot=None
        )

# Route: Reserve Slot Action
@app.route('/reserve-slot/<int:slot_id>', methods=['POST'])
@login_required
def reserve_slot(slot_id):
    user_id = session['user_id']
    vehicle_number = session['vehicle_number']

    # Check if user already has an active reservation
    active_booking = get_user_active_booking(user_id)
    if active_booking:
        flash(f"You already have an active reservation for slot {active_booking['slot_number']} (Ref: {active_booking['booking_reference']}).", 'warning')
        return redirect(url_for('my_booking'))

    db = get_db()
    cursor = db.cursor()

    # Atomically verify slot availability
    cursor.execute("SELECT * FROM parking_slots WHERE id = ?", (slot_id,))
    slot = cursor.fetchone()

    if not slot or slot['status'] != 'Available':
        flash(f"Slot {slot['slot_number'] if slot else ''} is no longer available. Please select another slot.", 'danger')
        return redirect(url_for('dashboard'))

    # Generate Booking Reference e.g. SP1001
    cursor.execute("SELECT COUNT(*) FROM bookings")
    booking_count = cursor.fetchone()[0] + 1
    booking_ref = f"SP{1000 + booking_count}"

    try:
        # Update slot status to Reserved
        cursor.execute('''
            UPDATE parking_slots 
            SET status = 'Reserved', vehicle_number = ? 
            WHERE id = ? AND status = 'Available'
        ''', (vehicle_number, slot_id))

        if cursor.rowcount == 0:
            flash("Reservation failed: Slot was taken by another request.", 'danger')
            return redirect(url_for('dashboard'))

        # Create booking record
        cursor.execute('''
            INSERT INTO bookings (booking_reference, user_id, slot_id, vehicle_number, status)
            VALUES (?, ?, ?, ?, 'Reserved')
        ''', (booking_ref, user_id, slot_id, vehicle_number))

        db.commit()
        flash(f"BOOKING CONFIRMED! Slot {slot['slot_number']} reserved under Reference: {booking_ref}", 'success')
        return redirect(url_for('my_booking'))

    except sqlite3.Error as e:
        db.rollback()
        flash("Database error during reservation. Please try again.", 'danger')
        return redirect(url_for('dashboard'))

# Route: Digital Parking Layout Page
@app.route('/parking')
def parking_layout():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM parking_slots ORDER BY slot_number ASC")
    slots = cursor.fetchall()
    return render_template('parking.html', slots=slots)

# Route: My Booking Page
@app.route('/booking')
@login_required
def my_booking():
    booking = get_user_active_booking(session['user_id'])
    return render_template('booking.html', booking=booking)

# Route: Cancel Booking Action
@app.route('/cancel-booking/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute('''
        SELECT b.*, p.slot_number 
        FROM bookings b 
        JOIN parking_slots p ON b.slot_id = p.id 
        WHERE b.id = ? AND b.user_id = ? AND b.status = 'Reserved'
    ''', (booking_id, session['user_id']))
    booking = cursor.fetchone()

    if not booking:
        flash("Invalid booking or reservation cannot be cancelled.", 'danger')
        return redirect(url_for('my_booking'))

    try:
        # Revert slot status back to Available
        cursor.execute('''
            UPDATE parking_slots 
            SET status = 'Available', vehicle_number = NULL 
            WHERE id = ?
        ''', (booking['slot_id'],))

        # Update booking status to Cancelled
        cursor.execute('''
            UPDATE bookings 
            SET status = 'Cancelled' 
            WHERE id = ?
        ''', (booking_id,))

        db.commit()
        flash(f"Reservation for Slot {booking['slot_number']} (Ref: {booking['booking_reference']}) has been cancelled.", 'info')
    except sqlite3.Error:
        db.rollback()
        flash("Failed to cancel reservation due to a database error.", 'danger')

    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    print("Starting Smart Parking Management System Flask Application...")
    app.run(debug=True, port=5000)
