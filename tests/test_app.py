import pytest
from app.app import app, reset_db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    reset_db()
    with app.test_client() as client:
        yield client

def test_health_check(client):
    res = client.get('/health')
    assert res.status_code == 200
    data = res.get_json()
    assert data['status'] == 'healthy'
    assert data['version'] == 'v1'

def test_empty_notifications(client):
    # Test GET /api/notifications returns empty list initially
    res = client.get('/api/notifications')
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    assert len(data) == 0

    # Test HTML UI shows empty state
    ui_res = client.get('/')
    assert ui_res.status_code == 200
    assert b"No notifications available" in ui_res.data

def test_add_notification_success(client):
    payload = {
        "title": "System Alert",
        "message": "High CPU utilization detected."
    }
    res = client.post('/api/notifications', json=payload)
    assert res.status_code == 201
    data = res.get_json()
    assert data['id'] == 1
    assert data['title'] == "System Alert"
    assert data['message'] == "High CPU utilization detected."
    assert 'timestamp' in data

    # Verify viewing notifications contains this alert
    list_res = client.get('/api/notifications')
    assert list_res.status_code == 200
    notifications = list_res.get_json()
    assert len(notifications) == 1
    assert notifications[0]['title'] == "System Alert"

def test_add_notification_invalid_inputs(client):
    # Missing title
    res1 = client.post('/api/notifications', json={"message": "Only message"})
    assert res1.status_code == 400
    assert "error" in res1.get_json()

    # Missing message
    res2 = client.post('/api/notifications', json={"title": "Only title"})
    assert res2.status_code == 400
    assert "error" in res2.get_json()

    # Empty strings
    res3 = client.post('/api/notifications', json={"title": "  ", "message": "   "})
    assert res3.status_code == 400

    # None payload
    res4 = client.post('/api/notifications', json={})
    assert res4.status_code == 400

def test_delete_notification_success(client):
    # Add an alert
    add_res = client.post('/api/notifications', json={"title": "To Delete", "message": "Delete this."})
    notif_id = add_res.get_json()['id']

    # Delete it
    del_res = client.delete(f'/api/notifications/{notif_id}')
    assert del_res.status_code == 200
    assert "deleted successfully" in del_res.get_json()['message']

    # Verify list is empty
    list_res = client.get('/api/notifications')
    assert len(list_res.get_json()) == 0

def test_delete_nonexistent_notification(client):
    res = client.delete('/api/notifications/999')
    assert res.status_code == 404
    assert "not found" in res.get_json()['error']

def test_html_form_add_and_delete(client):
    # Add via form
    res = client.post('/add', data={"title": "UI Alert", "message": "Form created alert"}, follow_redirects=True)
    assert res.status_code == 200
    assert b"UI Alert" in res.data
    assert b"Form created alert" in res.data

    # Invalid form add
    err_res = client.post('/add', data={"title": "", "message": ""})
    assert err_res.status_code == 400
    assert b"Title and Message are required" in err_res.data

    # Delete via form
    del_res = client.post('/delete/1', follow_redirects=True)
    assert del_res.status_code == 200
    assert b"No notifications available" in del_res.data

    # Delete nonexistent via form
    bad_del = client.post('/delete/999')
    assert bad_del.status_code == 404
    assert b"not found" in bad_del.data
