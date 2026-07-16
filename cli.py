import requests
import sys

BASE_URL = "http://127.0.0.1:5000"

# My function to check if server is running
def check_server():
    try:
        response = requests.get(f"{BASE_URL}/api", timeout=5)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False
    except Exception:
        return False

# My Main function for running the CLI application
def main():
    print("My Inventory CLI Application ")
    print("Welcome! Let us  manage our stock.\n")
    
    # Checking  if server is available
    if not check_server():
        print("Error: Cannot connect to server.")
        print("Please make sure the Flask app is running on http://127.0.0.1:5000")
        print("Start it with: pipenv run python app.py")
        sys.exit(1)
    
    while True:
        print("\nWhat would you like to do?")
        print("1. View all items")
        print("2. Add new item")
        print("3. Update item")
        print("4. Delete item")
        print("5. Search OpenFoodFacts")
        print("6. Add from OpenFoodFacts")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()

        if choice == "1":
            view_items()
        elif choice == "2":
            add_item()
        elif choice == "3":
            update_item()
        elif choice == "4":
            delete_item()
        elif choice == "5":
            search_product()
        elif choice == "6":
            add_from_external()
        elif choice == "7":
            print("Thank you for using the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

# My function to view all items in inventory
def view_items():
    try:
        response = requests.get(f"{BASE_URL}/items", timeout=10)
        data = response.json()
        print("\n Current Inventory")
        if not data.get("items"):
            print("No items yet.")
        else:
            for item in data["items"]:
                print(f"ID: {item['id']} | {item['name']} | Qty: {item['quantity']} | Price: Ksh {item['price']}")
    except requests.exceptions.Timeout:
        print("Error: Request timed out. Server may be slow.")
    except requests.exceptions.ConnectionError:
        print("Error: Lost connection to server.")
    except Exception as e:
        print(f"Error: Something went wrong - {str(e)}")

# My Function to add a new item through CLI
def add_item():
    print("\n Add New Item ")
    name = input("Enter item name: ").strip()
    
    # Validating the  name
    if not name:
        print("Error: Item name cannot be empty!")
        return
    
    if len(name) < 2:
        print("Error: Item name must be at least 2 characters!")
        return
    
    # Validating the  quantity
    try:
        quantity_input = input("Enter quantity: ").strip()
        if not quantity_input:
            print("Error: Quantity cannot be empty!")
            return
        
        quantity = int(quantity_input)
        if quantity < 0:
            print("Error: Quantity cannot be negative!")
            return
        if quantity > 999999:
            print("Error: Quantity seems too high!")
            return
            
    except ValueError:
        print("Error: Quantity must be a whole number!")
        return
    
    # Validating the  price
    try:
        price_input = input("Enter price (Ksh): ").strip()
        if not price_input:
            print("Error: Price cannot be empty!")
            return
        
        price = float(price_input)
        if price < 0:
            print("Error: Price cannot be negative!")
            return
        if price > 999999:
            print("Error: Price seems too high!")
            return
            
    except ValueError:
        print("Error: Price must be a number!")
        return
    
    # Sending a request
    try:
        response = requests.post(f"{BASE_URL}/items", json={
            "name": name,
            "quantity": quantity,
            "price": price
        }, timeout=10)
        
        if response.status_code == 201:
            result = response.json()
            print(result.get("message", "Item added successfully!"))
        elif response.status_code == 400:
            print("Error: Invalid data sent to server.")
        else:
            print(f"Error: Server returned status {response.status_code}")
        
    except requests.exceptions.Timeout:
        print("Error: Request timed out.")
    except requests.exceptions.ConnectionError:
        print("Error: Lost connection to server.")
    except Exception as e:
        print(f"Error: Could not add item - {str(e)}")

# My function to update an existing item
def update_item():
    print("\n Update Item ")
    
    # Validating the  item ID
    try:
        item_id_input = input("Enter item ID to update: ").strip()
        if not item_id_input:
            print("Error: Item ID cannot be empty!")
            return
        
        item_id = int(item_id_input)
        if item_id <= 0:
            print("Error: Item ID must be a positive number!")
            return
            
    except ValueError:
        print("Error: Item ID must be a number!")
        return
    
    # Checking  if the  item exists
    try:
        response = requests.get(f"{BASE_URL}/items/{item_id}", timeout=10)
        if response.status_code == 404:
            print("Error: Item not found.")
            return
        elif response.status_code != 200:
            print(f"Error: Server returned status {response.status_code}")
            return
    except Exception:
        print("Error: Could not verify item exists.")
        return
    
    print("Leave blank if you don't want to change a field.")
    
    # Get optional updates
    name = input("New name or press Enter to keep same: ").strip()
    quantity_input = input("New quantity or press Enter to keep same: ").strip()
    price_input = input("New price or press Enter to keep same: ").strip()
    
    # Build update data with only provided fields
    update_data = {}
    
    if name:
        if len(name) < 2:
            print("Error: Name must be at least 2 characters!")
            return
        update_data["name"] = name
    
    if quantity_input:
        try:
            qty = int(quantity_input)
            if qty < 0:
                print("Error: Quantity cannot be negative!")
                return
            update_data["quantity"] = qty
        except ValueError:
            print("Error: Quantity must be a whole number!")
            return
    
    if price_input:
        try:
            prc = float(price_input)
            if prc < 0:
                print("Error: Price cannot be negative!")
                return
            update_data["price"] = prc
        except ValueError:
            print("Error: Price must be a number!")
            return
    
    if not update_data:
        print("No changes made.")
        return
    
    # Sending  update request
    try:
        response = requests.patch(f"{BASE_URL}/items/{item_id}", json=update_data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(result.get("message", "Item updated successfully!"))
        elif response.status_code == 404:
            print("Error: Item not found.")
        else:
            print(f"Error: Server returned status {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("Error: Request timed out.")
    except requests.exceptions.ConnectionError:
        print("Error: Lost connection to server.")
    except Exception as e:
        print(f"Error: Could not update item - {str(e)}")

# My function to delete an item
def delete_item():
    print("\n Delete Item ")
    
    # Validating my  item ID
    try:
        item_id_input = input("Enter item ID to delete: ").strip()
        if not item_id_input:
            print("Error: Item ID cannot be empty!")
            return
        
        item_id = int(item_id_input)
        if item_id <= 0:
            print("Error: Item ID must be a positive number!")
            return
            
    except ValueError:
        print("Error: Item ID must be a number!")
        return
    
    # Confirming the  deletion
    confirm = input(f"Are you sure you want to delete item {item_id}? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Deletion cancelled.")
        return
    
    # Sending  delete request
    try:
        response = requests.delete(f"{BASE_URL}/items/{item_id}", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(result.get("message", "Item deleted successfully!"))
        elif response.status_code == 404:
            print("Error: Item not found.")
        else:
            print(f"Error: Server returned status {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("Error: Request timed out.")
    except requests.exceptions.ConnectionError:
        print("Error: Lost connection to server.")
    except Exception as e:
        print(f"Error: Could not delete item - {str(e)}")

# My function to search product from OpenFoodFacts
def search_product():
    query = input("Enter product name or barcode: ").strip()
    
    if not query:
        print("Error: Search term cannot be empty!")
        return
    
    if len(query) < 2:
        print("Error: Search term must be at least 2 characters!")
        return
    
    try:
        response = requests.get(f"{BASE_URL}/search?q={query}", timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print(f"\nFound: {data['product']['name']}")
                print(f"Brand: {data['product'].get('brand', 'N/A')}")
                print(f"Category: {data['product'].get('category', 'N/A')}")
            else:
                print(data.get("error", "Product not found"))
        elif response.status_code == 404:
            print("Product not found in database.")
        else:
            print(f"Error: Server returned status {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("Error: Search timed out. Try again later.")
    except requests.exceptions.ConnectionError:
        print("Error: Lost connection to server.")
    except Exception as e:
        print(f"Error: Could not search - {str(e)}")

# My function to add a product from OpenFoodFacts to inventory
def add_from_external():
    print("\n Add from OpenFoodFacts")
    query = input("Enter product name or barcode: ").strip()
    
    if not query:
        print("Error: Search term cannot be empty!")
        return
    
    if len(query) < 2:
        print("Error: Search term must be at least 2 characters!")
        return
    
    # Validating  quantity
    try:
        qty_input = input("Enter quantity (default 1): ").strip()
        if qty_input:
            quantity = int(qty_input)
            if quantity < 1:
                print("Error: Quantity must be at least 1!")
                return
        else:
            quantity = 1
    except ValueError:
        print("Error: Quantity must be a whole number!")
        return
    
    try:
        response = requests.post(f"{BASE_URL}/items/external", json={
            "barcode": query,
            "quantity": quantity
        }, timeout=15)
        
        if response.status_code == 201:
            result = response.json()
            print(result.get("message", "Item added from external source!"))
        elif response.status_code == 400:
            print("Error: Invalid data sent to server.")
        else:
            print(f"Error: Server returned status {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("Error: Request timed out.")
    except requests.exceptions.ConnectionError:
        print("Error: Lost connection to server.")
    except Exception as e:
        print(f"Error: Could not add item - {str(e)}")

# My  Main function for running the CLI application
if __name__ == "__main__":
    main()