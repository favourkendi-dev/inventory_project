import requests

BASE_URL = "http://127.0.0.1:5000"

# Main function for running the CLI application
def main():
    print(" My Inventory CLI Application ")
    print("Welcome! Let's manage our stock.\n")
    
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
            print("Invalid choice. Please try again.")

# My function to view all items in inventory
def view_items():
    try:
        response = requests.get(f"{BASE_URL}/items")
        data = response.json()
        print("\n Current Inventory ")
        if not data.get("items"):
            print("No items yet.")
        else:
            for item in data["items"]:
                print(f"ID: {item['id']} | {item['name']} | Qty: {item['quantity']} | Price: Ksh {item['price']}")
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to server. Is the Flask app running?")
    except Exception:
        print("Something went wrong while fetching items.")

# My Function to add a new item through CLI
def add_item():
    print("\n Add New Item ")
    name = input("Enter item name: ").strip()
    
    if not name:
        print("Error: Item name is required!")
        return
    
    try:
        quantity = int(input("Enter quantity: "))
        price = float(input("Enter price (Ksh): "))
        
        response = requests.post(f"{BASE_URL}/items", json={
            "name": name,
            "quantity": quantity,
            "price": price
        })
        
        result = response.json()
        print(result.get("message", "Item added successfully!"))
        
    except ValueError:
        print("Error: Please enter valid numbers for quantity and price.")
    except Exception:
        print("Could not connect to server. Make sure Flask app is running.")

# My function to update an existing item
def update_item():
    print("\n Update Item ")
    try:
        item_id = int(input("Enter item ID to update: "))
        
        # First we will check if item exists
        response = requests.get(f"{BASE_URL}/items/{item_id}")
        if response.status_code == 404:
            print("Error: Item not found.")
            return
        
        print("Leave blank if you don't want to change a field.")
        
        name = input("New name (or press Enter to keep same): ").strip()
        quantity_input = input("New quantity (or press Enter to keep same): ").strip()
        price_input = input("New price (or press Enter to keep same): ").strip()
        
        # Build update data with only provided fields
        update_data = {}
        if name:
            update_data["name"] = name
        if quantity_input:
            update_data["quantity"] = int(quantity_input)
        if price_input:
            update_data["price"] = float(price_input)
        
        if not update_data:
            print("No changes made.")
            return
        
        response = requests.patch(f"{BASE_URL}/items/{item_id}", json=update_data)
        result = response.json()
        print(result.get("message", "Item updated successfully!"))
        
    except ValueError:
        print("Error: Please enter valid numbers.")
    except Exception:
        print("Could not update item. Check if server is running.")

# My function to delete an item
def delete_item():
    print("\n Delete Item ")
    try:
        item_id = int(input("Enter item ID to delete: "))
        
        confirm = input(f"Are you sure you want to delete item {item_id}? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Deletion cancelled.")
            return
        
        response = requests.delete(f"{BASE_URL}/items/{item_id}")
        
        if response.status_code == 404:
            print("Error: Item not found.")
            return
        
        result = response.json()
        print(result.get("message", "Item deleted successfully!"))
        
    except ValueError:
        print("Error: Please enter a valid item ID.")
    except Exception:
        print("Could not delete item. Check if server is running.")

# My function to search product from OpenFoodFacts
def search_product():
    query = input("Enter product name or barcode: ").strip()
    if not query:
        print("Please enter a search term.")
        return
    
    try:
        response = requests.get(f"{BASE_URL}/search?q={query}")
        data = response.json()
        if data.get("success"):
            print(f"\nFound: {data['product']['name']}")
            print(f"Brand: {data['product'].get('brand', 'N/A')}")
            print(f"Category: {data['product'].get('category', 'N/A')}")
        else:
            print(data.get("error", "Product not found"))
    except Exception:
        print("Could not connect to server.")

# My function to add a product from OpenFoodFacts to inventory
def add_from_external():
    print("\n Add from OpenFoodFacts")
    query = input("Enter product name or barcode: ").strip()
    
    if not query:
        print("Please enter a search term.")
        return
    
    try:
        response = requests.post(f"{BASE_URL}/items/from-external", json={
            "barcode": query,
            "quantity": 1
        })
        
        result = response.json()
        print(result.get("message", "Item added from external source!"))
        
    except Exception:
        print("Could not add item from external source. Check if server is running.")

# My  Main function for running the CLI application
if __name__ == "__main__":
    main()