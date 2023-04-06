import pytest
from TA import main

@pytest.fixture
def client():
    with main.app.test_client() as client:
        yield client

def test_view_all(client):
    response = client.get('/viewAll')
    assert response.status_code == 500 # test without token authentication

def test_view_all_id(client):
    response = client.get('/viewAllId')
    assert response.status_code == 500 # test without token authentication

def test_view_with_id(client):
    response = client.get('/viewWithId/1')
    assert response.status_code == 500 # test without token authentication

def test_add(client):
    data = {
        'id': 1,
        'native_english_speaker': True,
        'course_instructor': 21,
        'course': 12,
        'semester': True,
        'class_size': 20,
        'performance_score': 2
    }
    response = client.post('/add', data=data)
    assert response.status_code == 500 # test without token authentication

def test_update(client):
    data = {
        'native_english_speaker': True,
        'course_instructor': 'Jane Doe',
        'course': 'Science',
        'semester': True,
        'class_size': 30,
        'performance_score': 85
    }
    response = client.put('/update/1', data=data)
    assert response.status_code == 500 # test without token authentication

def test_delete(client):
    response = client.post('/delete/1')
    assert response.status_code == 500 # test without token authentication

def test_login(client):
    data = {
        'email': 'khizar@gmail.com',
        'password': '12345678'
    }
    response = client.post('/login', data=data)
    assert response.status_code == 200

def test_signup(client):
    data = {
        'email': 'newuser@example.com',
        'password': 'password'
    }
    response = client.post('/signup', data=data)
    assert response.status_code == 200
    assert response.json['Success'] == 'User added Successfully'
