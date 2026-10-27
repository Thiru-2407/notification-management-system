import os
import sqlite3
from datetime import datetime, timezone
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, g

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-v3-production-ready'
DB_PATH = os.environ.get('DATABASE_PATH', os.path.join(os.path.dirname(__file__), 'notifications_v3.db'))

VALID_PRIORITIES = {'INFO', 'WARNING', 'CRITICAL', 'SUCCESS'}

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
                priority TEXT NOT NULL DEFAULT 'INFO',
                timestamp TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

init_db()

def validate_notification_data(title, message, priority='INFO'):
    errors = []
    if not title or not isinstance(title, str):
        errors.append("Title is required.")
    else:
        cleaned_title = title.strip()
        if len(cleaned_title) < 3:
            errors.append("Title must be at least 3 characters long.")
        elif len(cleaned_title) > 100:
            errors.append("Title cannot exceed 100 characters.")

    if not message or not isinstance(message, str):
        errors.append("Message is required.")
    else:
        cleaned_msg = message.strip()
        if len(cleaned_msg) < 5:
            errors.append("Message must be at least 5 characters long.")
        elif len(cleaned_msg) > 500:
            errors.append("Message cannot exceed 500 characters.")

    priority_upper = (priority or 'INFO').upper()
    if priority_upper not in VALID_PRIORITIES:
        errors.append(f"Invalid priority '{priority}'. Allowed: {', '.join(sorted(VALID_PRIORITIES))}")

    return errors, priority_upper

@app.errorhandler(400)
def bad_request(e):
    if request.path.startswith('/api/'):
        return jsonify({"error": "Bad Request", "details": str(e)}), 400
    flash(f"Bad Request: {e}", "danger")
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(e):
    if request.path.startswith('/api/'):
        return jsonify({"error": "Resource Not Found"}), 404
    return render_template('404.html', version="v3"), 404

@app.errorhandler(500)
def internal_error(e):
    if request.path.startswith('/api/'):
        return jsonify({"error": "Internal Server Error"}), 500
    return render_template('500.html', version="v3"), 500

@app.route('/')
def index():
    db = get_db()
    cursor = db.execute('SELECT id, title, message, priority, timestamp FROM notifications ORDER BY id DESC')
    notifications = [dict(row) for row in cursor.fetchall()]
    
    stats = {
        'total': len(notifications),
        'critical': sum(1 for n in notifications if n['priority'] == 'CRITICAL'),
        'warning': sum(1 for n in notifications if n['priority'] == 'WARNING'),
        'info': sum(1 for n in notifications if n['priority'] == 'INFO'),
        'success': sum(1 for n in notifications if n['priority'] == 'SUCCESS'),
    }
    return render_template('index.html', notifications=notifications, stats=stats, version="v3")

@app.route('/health')
def health():
    try:
        db = get_db()
        db.execute('SELECT 1').fetchone()
        db_healthy = True
    except Exception:
        db_healthy = False

    status_code = 200 if db_healthy else 503
    return jsonify({
        "status": "healthy" if db_healthy else "degraded",
        "version": "v3",
        "database": "connected" if db_healthy else "disconnected",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), status_code

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title', '').strip()
    message = request.form.get('message', '').strip()
    priority = request.form.get('priority', 'INFO').strip()

    errors, priority_upper = validate_notification_data(title, message, priority)
    if errors:
        for err in errors:
            flash(err, "danger")
        return redirect(url_for('index'))

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db = get_db()
    db.execute('INSERT INTO notifications (title, message, priority, timestamp) VALUES (?, ?, ?, ?)',
               (title, message, priority_upper, timestamp))
    db.commit()
    flash(f"Notification '{title}' created successfully.", "success")
    return redirect(url_for('index'))

@app.route('/delete/<int:notif_id>', methods=['POST'])
def delete(notif_id):
    db = get_db()
    cursor = db.execute('DELETE FROM notifications WHERE id = ?', (notif_id,))
    db.commit()

    if cursor.rowcount == 0:
        flash(f"Notification #{notif_id} could not be found.", "danger")
        return redirect(url_for('index')), 404

    flash(f"Notification #{notif_id} deleted successfully.", "success")
    return redirect(url_for('index'))

# REST API endpoints
@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    priority_filter = request.args.get('priority')
    db = get_db()
    if priority_filter and priority_filter.upper() in VALID_PRIORITIES:
        cursor = db.execute('SELECT id, title, message, priority, timestamp FROM notifications WHERE priority = ? ORDER BY id ASC',
                            (priority_filter.upper(),))
    else:
        cursor = db.execute('SELECT id, title, message, priority, timestamp FROM notifications ORDER BY id ASC')
    
    rows = [dict(row) for row in cursor.fetchall()]
    return jsonify(rows), 200

@app.route('/api/notifications', methods=['POST'])
def create_notification():
    data = request.get_json(silent=True) or {}
    title = data.get('title', '')
    message = data.get('message', '')
    priority = data.get('priority', 'INFO')

    errors, priority_upper = validate_notification_data(title, message, priority)
    if errors:
        return jsonify({"error": "Validation failed", "details": errors}), 400

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db = get_db()
    cursor = db.execute('INSERT INTO notifications (title, message, priority, timestamp) VALUES (?, ?, ?, ?)',
                        (title.strip(), message.strip(), priority_upper, timestamp))
    db.commit()
    new_id = cursor.lastrowid

    new_notif = {
        'id': new_id,
        'title': title.strip(),
        'message': message.strip(),
        'priority': priority_upper,
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
    port = int(os.environ.get('PORT', 8083))
    app.run(host='0.0.0.0', port=port, debug=False)
