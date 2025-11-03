"""
Database initialization and helper functions for authentication
"""
import sqlite3
import os
from werkzeug.security import generate_password_hash

DATABASE_PATH = 'data/crop_predictor.db'

def get_db():
    """Get database connection"""
    db = sqlite3.connect(DATABASE_PATH)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    """Initialize database with required tables"""
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    db = get_db()
    cursor = db.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'farmer')),
            full_name TEXT,
            location TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create predictions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            commodity TEXT NOT NULL,
            state TEXT NOT NULL,
            rainfall REAL,
            temperature REAL,
            month INTEGER,
            year INTEGER,
            predicted_price REAL NOT NULL,
            prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Migrate old 'location' column to 'state' if it exists
    try:
        cursor.execute("PRAGMA table_info(predictions)")
        columns = [column[1] for column in cursor.fetchall()]
        if 'location' in columns and 'state' not in columns:
            # Rename location to state
            cursor.execute("ALTER TABLE predictions RENAME COLUMN location TO state")
            print("✅ Migrated predictions table: location → state")
    except Exception as e:
        pass  # Table doesn't exist or already migrated
    
    # Create default admin if not exists
    cursor.execute('SELECT id FROM users WHERE username = ?', ('admin',))
    if not cursor.fetchone():
        admin_password = generate_password_hash('admin123')  # Change in production!
        cursor.execute(
            'INSERT INTO users (username, password_hash, role, full_name) VALUES (?, ?, ?, ?)',
            ('admin', admin_password, 'admin', 'Administrator')
        )
    
    # Create default farmer for testing
    cursor.execute('SELECT id FROM users WHERE username = ?', ('farmer',))
    if not cursor.fetchone():
        farmer_password = generate_password_hash('farmer123')
        cursor.execute(
            'INSERT INTO users (username, password_hash, role, full_name, location) VALUES (?, ?, ?, ?, ?)',
            ('farmer', farmer_password, 'farmer', 'Test Farmer', 'Maharashtra')
        )
    
    db.commit()
    db.close()
    print("✅ Database initialized successfully!")

def close_db(db):
    """Close database connection"""
    if db is not None:
        db.close()

if __name__ == '__main__':
    init_db()

