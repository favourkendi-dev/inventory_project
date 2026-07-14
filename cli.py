import requests
import json

BASE_URL = "http://127.0.0.1:5000"

# My Function to view all items in inventory
def main():
    print("My Inventory CLI Application")
    print("1. View all items")
    print("2. Add new item")
    print("3. Search OpenFoodFacts")
    print("4. Exit")

    while True:
        choice = input("\nEnter your choice (1-4): ")

        if choice == "1":
            view_items()
        elif choice == "2":
            add_item()
        elif choice == "3":
            search_product()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

# My function to view items in inventory
def view_items():
    try:
        response = requests.get(f"{BASE_URL}/items")
        data = response.json()
        print("\nCurrent Inventory ")
        if not data["items"]:
            print("No items yet.")
        else:
            for item in data["items"]:
                print(f"ID: {item['id']} | {item['name']} | Qty: {item['quantity']} | Price: {item['price']}")
    except:
        print("Could not connect to server. Make sure the Flask app is running.")

# My Function to add a new item through CLI
def add_item():
    name = input("Enter item name: ")
    quantity = int(input("Enter quantity: "))
    price = float(input("Enter price: "))

    try:
        response = requests.post(f"{BASE_URL}/items", json={
            "name": name,
            "quantity": quantity,
            "price": price
        })
        print(response.json()["message"])
    except:
        print("Could not connect to server.")