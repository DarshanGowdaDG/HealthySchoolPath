import sqlite3
import pandas as pd
from datetime import datetime

def init_db():
    conn = sqlite3.connect('health_education.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create progress table
    c.execute('''
        CREATE TABLE IF NOT EXISTS progress (
            username TEXT,
            section TEXT,
            activity TEXT,
            value REAL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (username) REFERENCES users(username)
        )
    ''')
    
    # Create streaks table
    c.execute('''
        CREATE TABLE IF NOT EXISTS streaks (
            username TEXT,
            activity TEXT,
            current_streak INTEGER DEFAULT 0,
            last_activity_date DATE,
            FOREIGN KEY (username) REFERENCES users(username),
            PRIMARY KEY (username, activity)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect('health_education.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                 (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(username, password):
    conn = sqlite3.connect('health_education.db')
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    conn.close()
    return result and result[0] == password

def update_progress(username, section, activity, value):
    conn = sqlite3.connect('health_education.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO progress (username, section, activity, value)
        VALUES (?, ?, ?, ?)
    ''', (username, section, activity, value))
    conn.commit()
    conn.close()

def get_progress(username, section=None):
    conn = sqlite3.connect('health_education.db')
    query = '''
        SELECT section, activity, value, date
        FROM progress
        WHERE username = ?
    '''
    params = [username]
    
    if section:
        query += ' AND section = ?'
        params.append(section)
        
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def update_streak(username, activity):
    conn = sqlite3.connect('health_education.db')
    c = conn.cursor()
    today = datetime.now().date()
    # Check if a record already exists for this user and activity
    c.execute('SELECT current_streak, last_activity_date FROM streaks WHERE username = ? AND activity = ?', 
             (username, activity))
    result = c.fetchone()
    
    if result:
        current_streak, last_date_str = result
        last_date = datetime.strptime(last_date_str, '%Y-%m-%d').date() if isinstance(last_date_str, str) else last_date_str
        
        # Update the streak based on date difference
        if last_date == today:
            # Already logged today, no change
            pass
        elif (today - last_date).days == 1:
            # Consecutive day, increment streak
            current_streak += 1
        else:
            # Streak broken, reset to 1
            current_streak = 1
            
        # Update existing record
        c.execute('''
            UPDATE streaks 
            SET current_streak = ?, last_activity_date = ? 
            WHERE username = ? AND activity = ?
        ''', (current_streak, today, username, activity))
    else:
        # Insert new record with streak of 1
        c.execute('''
            INSERT INTO streaks (username, activity, current_streak, last_activity_date) 
            VALUES (?, ?, 1, ?)
        ''', (username, activity, today))
    
    conn.commit()
    conn.close()