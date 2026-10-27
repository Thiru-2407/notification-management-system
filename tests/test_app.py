import os
import pytest
import sqlite3
import versions.v2.app.app as v2_app
from versions.v2.app.app import app

TEST_DB = os.path.join(os.path.dirname(__file__), 'test_v2.db')

@pytest.fixture
def client():
    v2_app.DB_PATH = TEST_DB
    app.config['TESTING'] = True

    # Re-initialize fresh database
    with sqlite3.connect(TEST_DB) as conn:
        conn.execute('DROP TABLE IF EXISTS notifications')
        conn.execute('''
            CREATE TABLE notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        conn.commit()

    with app.test_client() as client:
        yield client

    # Cleanup after test
    try:
        with sqlite3.connect(TEST_DB) as conn:
            conn.execute('DROP TABLE IF EXISTS notifications')
    except Exception:
        pass

def test_v2_health_check(client):
    res = client.get('/health')
    assert res.status_code == 200
    data = res.get_json()
    assert data['version'] == 'v2'
    assert data['storage'] == 'sqlite'

def test_v2_empty_state(client):
    res = client.get('/api/notifications')
    assert res.status_code == 200
    assert res.get_json() == []

    ui_res = client.get('/')
    assert ui_res.status_code == 200
    assert b"No Alerts Found" in ui_res.data

def test_v2_add_success_and_persistence(client):
    payload = {
        "title": "Persistent Alert v2",
        "message": "This record is stored inside SQLite database."
    }
    res = client.post('/api/notifications', json=payload)
    assert res.status_code == 201
    data = res.get_json()
    assert data['id'] == 1
    assert data['title'] == "Persistent Alert v2"
    assert "timestamp" in data

    # Verify query returns item
    list_res = client.get('/api/notifications')
    assert len(list_res.get_json()) == 1
    assert list_res.get_json()[0]['id'] == 1

def test_v2_input_validation(client):
    # Short title (< 3 chars)
    r1 = client.post('/api/notifications', json={"title": "AB", "message": "Valid message here"})
    assert r1.status_code == 400
    assert "at least 3 characters" in " ".join(r1.get_json()['details'])

    # Long title (> 100 chars)
    r2 = client.post('/api/notifications', json={"title": "A" * 101, "message": "Valid message here"})
    assert r2.status_code == 400
    assert "cannot exceed 100 characters" in " ".join(r2.get_json()['details'])

    # Short message (< 5 chars)
    r3 = client.post('/api/notifications', json={"title": "Valid Title", "message": "Hey"})
    assert r3.status_code == 400
    assert "at least 5 characters" in " ".join(r3.get_json()['details'])

    # Long message (> 500 chars)
    r4 = client.post('/api/notifications', json={"title": "Valid Title", "message": "M" * 501})
    assert r4.status_code == 400
    assert "cannot exceed 500 characters" in " ".join(r4.get_json()['details'])

def test_v2_delete_existing_and_nonexistent(client):
    # Add record
    add_res = client.post('/api/notifications', json={"title": "Delete Target", "message": "Record to be deleted"})
    notif_id = add_res.get_json()['id']

    # Delete existing
    del_res = client.delete(f'/api/notifications/{notif_id}')
    assert del_res.status_code == 200

    # Delete nonexistent
    del_bad = client.delete(f'/api/notifications/999')
    assert del_bad.status_code == 404
    assert "not found" in del_bad.get_json()['error']

def test_v2_ui_form_operations(client):
    # Add via form
    res = client.post('/add', data={"title": "Form Alert", "message": "Submitted via browser form"}, follow_redirects=True)
    assert res.status_code == 200
    assert b"Form Alert" in res.data

    # Validation failure in form
    bad_form = client.post('/add', data={"title": "X", "message": "Y"})
    assert bad_form.status_code == 400
    assert b"characters long" in bad_form.data
