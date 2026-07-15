import requests

BASE_URL = "https://world.openfoodfacts.org/api/v2"

# My headers for OpenFoodFacts because it requires a User-Agent
HEADERS = {
    "User-Agent": "InventoryApp/1.0 (favourkendi0@gmail.com)"
}


# My function to search product using barcode
def search_product_by_barcode(barcode):
    """Search product using barcode"""
    try:
        print(f"Searching barcode: {barcode}")
        
        url = f"{BASE_URL}/product/{barcode}.json"
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
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
    """Search product by name using API v2"""
    try:
        print(f"Searching by name: {name}")
        
        url = f"{BASE_URL}/search"
        params = {
            "search_terms2": name,
            "page_size": 5,
            "fields": "product_name,brands,categories,code,nutriments"
        }
        
        response = requests.get(url, params=params, headers=HEADERS, timeout=10)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            print(f"Found {len(products)} products")
            
            if products:
                return products[0]
            else:
                print("No products found")
                return None
                
        else:
            print(f"Bad status code: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error searching product: {e}")
        return None