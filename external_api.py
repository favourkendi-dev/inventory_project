import requests

BASE_URL = "https://world.openfoodfacts.org/api/v0"

# My function to search product using barcode
def search_product_by_barcode(barcode):
    """Search product using barcode"""
    try:
        print(f"Searching barcode: {barcode}")   # for debugging
        response = requests.get(f"{BASE_URL}/product/{barcode}.json", timeout=10)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Status in response: {data.get('status')}")
            if data.get('status') == 1:
                return data.get('product')
            else:
                print("Product not found in database")
                return None
        else:
            print(f"Bad status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# My function to search product by name
def search_product_by_name(name):
    """Search product by name"""
    try:
        response = requests.get(f"{BASE_URL}/search", params={
            "search_terms": name,
            "search_simple": 1,
            "action": "process",
            "json": 1
        }, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('products'):
                return data['products'][0]  # Return first result
        return None
    except Exception as e:
        print(f"Error searching product: {e}")
        return None