# Inventory Management System

A Flask based inventory management system with OpenFoodFacts API integration

## Features

- **Full CRUD Operations** — Create, Read, Update, Delete inventory items
- **OpenFoodFacts Integration** — Search and add products from external API
- **Web Interface** — Modern UI built with Tailwind CSS
- **Command Line Interface (CLI)** — Manage inventory from terminal
- **User Authentication** — Login and register with session management
- **Dashboard Stats** — View total items, total value, and low stock alerts
- **Local Search & Filter** — Search inventory items in real-time

## Installation & Setup

### Prerequisites
- Python 3.10+
- pipenv

### Step 1: Clone the Repository
```bash
git clone https://github.com/favourkendi-dev/inventory_project.git
cd inventory_project

## API Endpoints

| Endpoint | Method | Description | Auth Required |
|---|---|---|---|
| `/` | GET | Main web interface | Yes |
| `/api` | GET | Check API status | No |
| `/items` | GET | Get all inventory items | No (CLI) / Yes (Web) |
| `/items` | POST | Add new item | No (CLI) / Yes (Web) |
| `/items/&lt;id&gt;` | GET | Get single item by ID | Yes |
| `/items/&lt;id&gt;` | PATCH | Update item fields | Yes |
| `/items/&lt;id&gt;` | DELETE | Delete item | Yes |
| `/search` | GET | Search OpenFoodFacts API | No (CLI) / Yes (Web) |
| `/items/external` | POST | Add product from OpenFoodFacts | No (CLI) / Yes (Web) |
| `/login` | GET/POST | User login | No |
| `/register` | GET/POST | User registration | No |
| `/logout` | POST | User logout | Yes |
| `/check-session` | GET | Check login status | No |

### Request/Response Examples

**Add Item (POST /items)**
```json
// Request
{
  "name": "Rice",
  "quantity": 10,
  "price": 200.00
}

// Response
{
  "success": true,
  "message": "Successfully added Rice to inventory",
  "item": {
    "id": 1,
    "name": "Rice",
    "quantity": 10,
    "price": 200.00,
    "category": "General"
  }
}

## CLI Usage Examples

The CLI tool allows you to manage inventory from the terminal.

// Response
{
  "success": true,
  "product": {
    "name": "Nutella",
    "brand": "Ferrero",
    "category": "Spreads",
    "barcode": "3017624010701"
  }
}

### Start the CLI
```bash
pipenv run python cli.py

=== My Inventory CLI Application ===
Welcome! Let's manage our stock.

What would you like to do?
1. View all items
2. Add new item
3. Update item
4. Delete item
5. Search OpenFoodFacts
6. Add from OpenFoodFacts
7. Exit

Enter your choice (1-7): 1

--- Current Inventory ---
ID: 1 | Rice | Qty: 10 | Price: Ksh 200
ID: 2 | Sugar | Qty: 5 | Price: Ksh 150

Enter your choice (1-7): 5
Enter product name or barcode: nutella

Found: Nutella
Brand: Ferrero
Category: Spreads

Enter your choice (1-7): 3

--- Update Item ---
Enter item ID to update: 1
Leave blank if you don't want to change a field.
New name (or press Enter to keep same): Brown Rice
New quantity (or press Enter to keep same): 15
New price (or press Enter to keep same): 250
Item updated successfully

Enter your choice (1-7): 4

--- Delete Item ---
Enter item ID to delete: 2
Are you sure you want to delete item 2? (yes/no): yes
Item deleted successfully