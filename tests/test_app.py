import pytest
import sys
import os
sys.path.insert(0, os.path.abspath('.'))
from app import app

# My basic test setup
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# My first test that check if home page loads
def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200

# Test to check if we can get items
def test_get_items(client):
    response = client.get('/items')
    assert response.status_code == 200
    assert response.json["success"] == True

# Test adding an item
def test_add_item(client):
    response = client.post('/items', json={
        "name": "Test Item",
        "quantity": 10,
        "price": 100.0
    })
    assert response.status_code == 201
    assert response.json["success"] == True

if __name__ == "__main__":
    pytest.main()