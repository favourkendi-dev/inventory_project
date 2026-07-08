import requests

BASE_URL = "https://world.openfoodfacts.org/api/v0"

def search_product_by_barcode(barcode):
    """Search product using barcode"""
    try:
        response = requests.get(f"{BASE_URL}/product/{barcode}.json")
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 1:
                return data.get('product')
        return None
    except Exception as e:
        print(f"Error fetching product: {e}")
        return None

def search_product_by_name(name):
    """Search product by name"""
    try:
        response = requests.get(f"{BASE_URL}/search", params={
            "search_terms": name,
            "search_simple": 1,
            "action": "process",
            "json": 1
        })
        if response.status_code == 200:
            data = response.json()
            if data.get('products'):
                return data['products'][0]  # Return first result
        return None
    except Exception as e:
        print(f"Error searching product: {e}")
        return None