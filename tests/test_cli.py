import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path so we can import cli
sys.path.insert(0, os.path.abspath('.'))

import cli


# My test fixture for mock response
@pytest.fixture
def mock_response():
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {
        "success": True,
        "items": [],
        "total": 0
    }
    return response


# Test that check server returns True when server is running
@patch('cli.requests.get')
def test_check_server_success(mock_get):
    mock_get.return_value.status_code = 200
    result = cli.check_server()
    assert result == True


# Test that check server returns False when server is down
@patch('cli.requests.get')
def test_check_server_failure(mock_get):
    mock_get.side_effect = Exception("Connection error")
    result = cli.check_server()
    assert result == False


# Test view items when inventory is empty
@patch('cli.requests.get')
def test_view_items_empty(mock_get, mock_response):
    mock_get.return_value = mock_response
    mock_response.json.return_value = {"items": [], "total": 0}
    
    # Should not raise any errors
    cli.view_items()


# Test view items with items
@patch('cli.requests.get')
def test_view_items_with_data(mock_get, mock_response):
    mock_get.return_value = mock_response
    mock_response.json.return_value = {
        "items": [
            {"id": 1, "name": "Rice", "quantity": 10, "price": 200}
        ],
        "total": 1
    }
    
    # Should not raise any errors
    cli.view_items()


# Test add item with valid data
@patch('cli.requests.post')
@patch('builtins.input', side_effect=["Rice", "10", "200"])
def test_add_item_success(mock_input, mock_post, mock_response):
    mock_post.return_value = mock_response
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "success": True,
        "message": "Successfully added Rice to inventory"
    }
    
    cli.add_item()
    mock_post.assert_called_once()


# Test add item with empty name
@patch('builtins.input', side_effect=[""])
def test_add_item_empty_name(mock_input):
    # Should return early without making request
    cli.add_item()


# Test add item with negative quantity
@patch('builtins.input', side_effect=["Rice", "-5"])
def test_add_item_negative_quantity(mock_input):
    # Should return early without making request
    cli.add_item()


# Test delete item with valid ID
@patch('cli.requests.delete')
@patch('builtins.input', side_effect=["1", "yes"])
def test_delete_item_success(mock_input, mock_delete, mock_response):
    mock_delete.return_value = mock_response
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "success": True,
        "message": "Item deleted successfully"
    }
    
    cli.delete_item()
    mock_delete.assert_called_once()


# Test delete item when user cancels
@patch('builtins.input', side_effect=["1", "no"])
def test_delete_item_cancelled(mock_input):
    # Should return early without making request
    cli.delete_item()


# Test search product with valid query
@patch('cli.requests.get')
@patch('builtins.input', return_value="nutella")
def test_search_product_success(mock_input, mock_get, mock_response):
    mock_get.return_value = mock_response
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "success": True,
        "product": {
            "name": "Nutella",
            "brand": "Ferrero",
            "category": "Spreads"
        }
    }
    
    cli.search_product()
    mock_get.assert_called_once()


# Test search product with empty query
@patch('builtins.input', return_value="")
def test_search_product_empty(mock_input):
    # Should return early without making request
    cli.search_product()


# Test add from external with valid data
@patch('cli.requests.post')
@patch('builtins.input', side_effect=["nutella", "2"])
def test_add_from_external_success(mock_input, mock_post, mock_response):
    mock_post.return_value = mock_response
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "success": True,
        "message": "Added Nutella to inventory"
    }
    
    cli.add_from_external()
    mock_post.assert_called_once()


# Test add from external with empty query
@patch('builtins.input', return_value="")
def test_add_from_external_empty(mock_input):
    # Should return early without making request
    cli.add_from_external()