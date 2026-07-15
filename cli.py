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
        print("3. Search OpenFoodFacts")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            view_items()
        elif choice == "2":
            add_item()
        elif choice == "3":
            search_product()
        elif choice == "4":
            print("Thank you for using the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# My function to view all items in inventory
def view_items():
    try:
        response = requests.get(f"{BASE_URL}/items")
        data = response.json()
        print("\nCurrent Inventory ")
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
        else:
            print(data.get("error", "Product not found"))
    except Exception:
        print("Could not connect to server.")

if __name__ == "__main__":
    main()