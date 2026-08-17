import sqlite3
import os

def get_db_path():
    # Store database in the root project folder
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, 'parking.db')

def init_db():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            vehicle_number TEXT NOT NULL,
            vehicle_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create Parking Slots table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parking_slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slot_number TEXT UNIQUE NOT NULL,
            slot_type TEXT NOT NULL,
            status TEXT NOT NULL,
            vehicle_number TEXT
        )
    ''')

    # Create Bookings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_reference TEXT UNIQUE NOT NULL,
            user_id INTEGER NOT NULL,
            slot_id INTEGER NOT NULL,
            vehicle_number TEXT NOT NULL,
            booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            entry_time TIMESTAMP,
            exit_time TIMESTAMP,
            status TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (slot_id) REFERENCES parking_slots(id)
        )
    ''')

    # Check if slots are already populated
    cursor.execute('SELECT COUNT(*) FROM parking_slots')
    slot_count = cursor.fetchone()[0]

    if slot_count == 0:
        # Seed initial 12 parking slots as required for Week 3
        # Initial status setup:
        # A1: Available, A2: Occupied, A3: Available, A4: Available
        # B1: Occupied, B2: Available, B3: Available, B4: Occupied
        # C1: Available, C2: Available, C3: Occupied, C4: Available
        initial_slots = [
            ('A1', 'Car', 'Available', None),
            ('A2', 'Car', 'Occupied', 'KA01MH1122'),
            ('A3', 'Car', 'Available', None),
            ('A4', 'Car', 'Available', None),
            
            ('B1', 'Car', 'Occupied', 'KA02EX4455'),
            ('B2', 'Car', 'Available', None),
            ('B3', 'Car', 'Available', None),
            ('B4', 'Car', 'Occupied', 'KA03ZZ7788'),
            
            ('C1', 'Car', 'Available', None),
            ('C2', 'Car', 'Available', None),
            ('C3', 'Car', 'Occupied', 'KA05AA9900'),
            ('C4', 'Car', 'Available', None),
        ]

        cursor.executemany('''
            INSERT INTO parking_slots (slot_number, slot_type, status, vehicle_number)
            VALUES (?, ?, ?, ?)
        ''', initial_slots)
        print("Database initialized and 12 parking slots seeded successfully.")
    else:
        print("Database already contains parking slots.")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
