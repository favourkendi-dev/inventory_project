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



# Test for external API search
def test_search_product(client):
    response = client.get('/search?q=test')
    assert response.status_code in [200, 404]  # Either success or not found is okay

# Test for invalid input when adding item
def test_add_item_invalid(client):
    response = client.post('/items', json={"quantity": 10})  # No name added
    assert response.status_code == 400

# My test for delete item
def test_delete_item(client):
    # First add an item
    client.post('/items', json={"name": "Test Delete", "quantity": 5})
    # Then delete the last item (assuming id = 1 for simplicity)
    response = client.delete('/items/1')
    assert response.status_code == 200

if __name__ == "__main__":
    pytest.main()