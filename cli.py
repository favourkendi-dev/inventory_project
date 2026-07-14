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