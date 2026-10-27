import os
import pytest
import sqlite3
import versions.v3.app.app as v3_app
from versions.v3.app.app import app

TEST_DB_V3 = os.path.join(os.path.dirname(__file__), 'test_v3.db')

@pytest.fixture
def client():
    v3_app.DB_PATH = TEST_DB_V3
    app.config['TESTING'] = True

    with sqlite3.connect(TEST_DB_V3) as conn:
        conn.execute('DROP TABLE IF EXISTS notifications')
        conn.execute('''
            CREATE TABLE notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                priority TEXT NOT NULL DEFAULT 'INFO',
                timestamp TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

    with app.test_client() as client:
        yield client

    try:
        with sqlite3.connect(TEST_DB_V3) as conn:
            conn.execute('DROP TABLE IF EXISTS notifications')
    except Exception:
        pass

def test_v3_health_check(client):
    res = client.get('/health')
    assert res.status_code == 200
    data = res.get_json()
    assert data['version'] == 'v3'
    assert data['status'] == 'healthy'
    assert data['database'] == 'connected'
    assert 'timestamp' in data

def test_v3_empty_notifications_and_stats(client):
    res = client.get('/api/notifications')
    assert res.status_code == 200
    assert res.get_json() == []

    ui_res = client.get('/')
    assert ui_res.status_code == 200
    assert b"All Systems Clear" in ui_res.data
    assert b"Total Alerts" in ui_res.data

def test_v3_add_notification_with_priorities(client):
    # Add Critical alert
    p1 = {"title": "Node Failure", "message": "Kubelet unresponsive on node-1", "priority": "CRITICAL"}
    r1 = client.post('/api/notifications', json=p1)
    assert r1.status_code == 201
    d1 = r1.get_json()
    assert d1['priority'] == 'CRITICAL'
    assert d1['id'] == 1

    # Add Warning alert
    p2 = {"title": "High Disk Usage", "message": "Root volume above 85% capacity", "priority": "WARNING"}
    r2 = client.post('/api/notifications', json=p2)
    assert r2.status_code == 201
    assert r2.get_json()['priority'] == 'WARNING'

    # Filter by priority
    crit_res = client.get('/api/notifications?priority=CRITICAL')
    assert crit_res.status_code == 200
    assert len(crit_res.get_json()) == 1
    assert crit_res.get_json()[0]['title'] == "Node Failure"

def test_v3_validation_rules(client):
    # Invalid priority
    r_bad_p = client.post('/api/notifications', json={"title": "Valid Title", "message": "Valid Message", "priority": "UNKNOWN"})
    assert r_bad_p.status_code == 400
    assert "Invalid priority" in " ".join(r_bad_p.get_json()['details'])

    # Title too short
    r_short = client.post('/api/notifications', json={"title": "NO", "message": "Valid Message"})
    assert r_short.status_code == 400

    # Message too short
    r_short_m = client.post('/api/notifications', json={"title": "Valid Title", "message": "Tiny"})
    assert r_short_m.status_code == 400

    # Non-string data
    r_non_str = client.post('/api/notifications', json={"title": 12345, "message": None})
    assert r_non_str.status_code == 400

def test_v3_delete_operations(client):
    # Add alert
    add = client.post('/api/notifications', json={"title": "To Delete", "message": "Testing v3 deletion endpoint"})
    notif_id = add.get_json()['id']

    # Delete existing
    del_ok = client.delete(f'/api/notifications/{notif_id}')
    assert del_ok.status_code == 200
    assert "deleted successfully" in del_ok.get_json()['message']

    # Delete non-existent ID
    del_missing = client.delete('/api/notifications/9999')
    assert del_missing.status_code == 404
    assert "not found" in del_missing.get_json()['error']

def test_v3_ui_workflow(client):
    # Form post add
    res = client.post('/add', data={"title": "UI Cluster Alert", "message": "Dispatched via enterprise web dashboard", "priority": "SUCCESS"}, follow_redirects=True)
    assert res.status_code == 200
    assert b"created successfully" in res.data
    assert b"UI Cluster Alert" in res.data

    # Form post delete
    del_ui = client.post('/delete/1', follow_redirects=True)
    assert del_ui.status_code == 200
    assert b"deleted successfully" in del_ui.data
