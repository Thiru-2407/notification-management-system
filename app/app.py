import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-v1'

# In-memory storage for v1
notifications = []
current_id = 1

def reset_db():
    global notifications, current_id
    notifications = []
    current_id = 1

@app.route('/')
def index():
    return render_template('index.html', notifications=notifications, version="v1")

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "version": "v1"}), 200

@app.route('/add', methods=['POST'])
def add():
    global current_id
    title = request.form.get('title', '').strip()
    message = request.form.get('message', '').strip()

    if not title or not message:
        return render_template('index.html', notifications=notifications, error="Title and Message are required.", version="v1"), 400

    new_notif = {
        'id': current_id,
        'title': title,
        'message': message,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    notifications.append(new_notif)
    current_id += 1
    return redirect(url_for('index'))

@app.route('/delete/<int:notif_id>', methods=['POST'])
def delete(notif_id):
    global notifications
    found = False
    for notif in notifications:
        if notif['id'] == notif_id:
            found = True
            break
    
    if not found:
        return render_template('index.html', notifications=notifications, error=f"Notification with ID {notif_id} not found.", version="v1"), 404
        
    notifications = [n for n in notifications if n['id'] != notif_id]
    return redirect(url_for('index'))

# REST API endpoints for automated testing and programmatic access
@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    return jsonify(notifications), 200

@app.route('/api/notifications', methods=['POST'])
def create_notification():
    global current_id
    data = request.get_json(silent=True) or {}
    title = data.get('title', '').strip()
    message = data.get('message', '').strip()

    if not title or not message:
        return jsonify({"error": "Title and Message are required."}), 400

    new_notif = {
        'id': current_id,
        'title': title,
        'message': message,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    notifications.append(new_notif)
    current_id += 1
    return jsonify(new_notif), 201

@app.route('/api/notifications/<int:notif_id>', methods=['DELETE'])
def delete_notification(notif_id):
    global notifications
    original_len = len(notifications)
    notifications = [n for n in notifications if n['id'] != notif_id]
    if len(notifications) == original_len:
        return jsonify({"error": f"Notification with ID {notif_id} not found."}), 404
    return jsonify({"message": f"Notification {notif_id} deleted successfully."}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8081))
    app.run(host='0.0.0.0', port=port, debug=False)
