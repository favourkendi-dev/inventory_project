import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath('.'))

from external_api import search_product_by_barcode, search_product_by_name


# My test fixture for mock response
@pytest.fixture
def mock_success_response():
    response = MagicMock()
    response.status_code = 200
    return response


# Test search by barcode with successful result
@patch('external_api.requests.get')
def test_search_barcode_success(mock_get, mock_success_response):
    mock_get.return_value = mock_success_response
    mock_success_response.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Nutella",
            "brands": "Ferrero",
            "categories": "Spreads",
            "code": "3017624010701",
            "nutriments": {
                "energy_100g": 2252
            }
        }
    }
    
    result = search_product_by_barcode("3017624010701")
    
    assert result is not None
    assert result["product_name"] == "Nutella"
    assert result["brands"] == "Ferrero"


# Testing  search by barcode 
@patch('external_api.requests.get')
def test_search_barcode_not_found(mock_get, mock_success_response):
    mock_get.return_value = mock_success_response
    mock_success_response.json.return_value = {
        "status": 0,
        "product": {}
    }
    
    result = search_product_by_barcode("0000000000000")
    
    assert result is None


# Test search by barcode - API returns 404
@patch('external_api.requests.get')
def test_search_barcode_api_error(mock_get):
    error_response = MagicMock()
    error_response.status_code = 404
    mock_get.return_value = error_response
    
    result = search_product_by_barcode("12345")
    
    assert result is None


# Testing  search by barcoder
@patch('external_api.requests.get')
def test_search_barcode_connection_error(mock_get):
    mock_get.side_effect = Exception("Connection timeout")
    
    result = search_product_by_barcode("12345")
    
    assert result is None


# Test search by name with successful result
@patch('external_api.requests.get')
def test_search_name_success(mock_get, mock_success_response):
    mock_get.return_value = mock_success_response
    mock_success_response.json.return_value = {
        "products": [
            {
                "product_name": "Coca Cola",
                "brands": "Coca-Cola Company",
                "categories": "Beverages",
                "code": "5449000000996",
                "nutriments": {
                    "sugars_100g": 10.6
                }
            }
        ]
    }
    
    result = search_product_by_name("coca cola")
    
    assert result is not None
    assert result["product_name"] == "Coca Cola"
    assert result["brands"] == "Coca-Cola Company"


# Testing search by name 
@patch('external_api.requests.get')
def test_search_name_empty(mock_get, mock_success_response):
    mock_get.return_value = mock_success_response
    mock_success_response.json.return_value = {
        "products": []
    }
    
    result = search_product_by_name("xyznonexistent")
    
    assert result is None


# Testing  search by name 
@patch('external_api.requests.get')
def test_search_name_api_error(mock_get):
    error_response = MagicMock()
    error_response.status_code = 500
    mock_get.return_value = error_response
    
    result = search_product_by_name("test")
    
    assert result is None


# Testing  search by name 
@patch('external_api.requests.get')
def test_search_name_timeout(mock_get):
    mock_get.side_effect = Exception("Timeout")
    
    result = search_product_by_name("test")
    
    assert result is None


# Test that correct URL is used for barcode search
@patch('external_api.requests.get')
def test_search_barcode_correct_url(mock_get, mock_success_response):
    mock_get.return_value = mock_success_response
    mock_success_response.json.return_value = {
        "status": 1,
        "product": {"product_name": "Test"}
    }
    
    search_product_by_barcode("12345")
    
    # Check that the URL contains the barcode
    call_args = mock_get.call_args
    assert "12345" in str(call_args)


# Test that correct parameters are used for name search
@patch('external_api.requests.get')
def test_search_name_correct_params(mock_get, mock_success_response):
    mock_get.return_value = mock_success_response
    mock_success_response.json.return_value = {
        "products": [{"product_name": "Test"}]
    }
    
    search_product_by_name("banana")
    
    # Check that search terms2 parameter is used
    call_kwargs = mock_get.call_args[1]
    assert "params" in call_kwargs
    assert call_kwargs["params"]["search_terms2"] == "banana"