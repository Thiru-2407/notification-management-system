import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify, g

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-v2'
DB_PATH = os.environ.get('DATABASE_PATH', os.path.join(os.path.dirname(__file__), 'notifications_v2.db'))

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        conn.commit()

# Ensure DB is created at startup
init_db()

def validate_input(title, message):
    errors = []
    if not title or len(title.strip()) < 3:
        errors.append("Title must be at least 3 characters long.")
    elif len(title.strip()) > 100:
        errors.append("Title cannot exceed 100 characters.")

    if not message or len(message.strip()) < 5:
        errors.append("Message must be at least 5 characters long.")
    elif len(message.strip()) > 500:
        errors.append("Message cannot exceed 500 characters.")

    return errors

@app.route('/')
def index():
    db = get_db()
    cursor = db.execute('SELECT id, title, message, timestamp FROM notifications ORDER BY id DESC')
    rows = [dict(row) for row in cursor.fetchall()]
    return render_template('index.html', notifications=rows, version="v2")

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "version": "v2", "storage": "sqlite"}), 200

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title', '').strip()
    message = request.form.get('message', '').strip()

    errors = validate_input(title, message)
    if errors:
        db = get_db()
        cursor = db.execute('SELECT id, title, message, timestamp FROM notifications ORDER BY id DESC')
        rows = [dict(row) for row in cursor.fetchall()]
        return render_template('index.html', notifications=rows, error=" | ".join(errors), version="v2"), 400

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db = get_db()
    db.execute('INSERT INTO notifications (title, message, timestamp) VALUES (?, ?, ?)',
               (title, message, timestamp))
    db.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:notif_id>', methods=['POST'])
def delete(notif_id):
    db = get_db()
    cursor = db.execute('DELETE FROM notifications WHERE id = ?', (notif_id,))
    db.commit()

    if cursor.rowcount == 0:
        cursor2 = db.execute('SELECT id, title, message, timestamp FROM notifications ORDER BY id DESC')
        rows = [dict(row) for row in cursor2.fetchall()]
        return render_template('index.html', notifications=rows, error=f"Notification with ID {notif_id} not found.", version="v2"), 404

    return redirect(url_for('index'))

# REST API endpoints
@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    db = get_db()
    cursor = db.execute('SELECT id, title, message, timestamp FROM notifications ORDER BY id ASC')
    rows = [dict(row) for row in cursor.fetchall()]
    return jsonify(rows), 200

@app.route('/api/notifications', methods=['POST'])
def create_notification():
    data = request.get_json(silent=True) or {}
    title = data.get('title', '').strip()
    message = data.get('message', '').strip()

    errors = validate_input(title, message)
    if errors:
        return jsonify({"error": "Validation failed", "details": errors}), 400

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db = get_db()
    cursor = db.execute('INSERT INTO notifications (title, message, timestamp) VALUES (?, ?, ?)',
                        (title, message, timestamp))
    db.commit()
    new_id = cursor.lastrowid

    new_notif = {
        'id': new_id,
        'title': title,
        'message': message,
        'timestamp': timestamp
    }
    return jsonify(new_notif), 201

@app.route('/api/notifications/<int:notif_id>', methods=['DELETE'])
def delete_notification(notif_id):
    db = get_db()
    cursor = db.execute('DELETE FROM notifications WHERE id = ?', (notif_id,))
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({"error": f"Notification with ID {notif_id} not found."}), 404

    return jsonify({"message": f"Notification {notif_id} deleted successfully."}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8082))
    app.run(host='0.0.0.0', port=port, debug=False)
