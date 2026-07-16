# Inventory Management System

A Flask-based inventory management system with OpenFoodFacts API integration

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
```

### Step 2: Install Dependencies
```bash
pipenv install
```

### Step 3: Activate Virtual Environment
```bash
pipenv shell
```

### Step 4: Run the Flask App
```bash
pipenv run python app.py
```

### Step 5: Open in Browser
Visit: http://127.0.0.1:5000/

### Step 6: Run CLI (Optional)
In a new terminal:
```bash
pipenv run python cli.py
```


## Request/Response Examples

### Add Item (POST /items)
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
```

### Search OpenFoodFacts (GET /search?q=nutella)
```json
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
```

## CLI Usage Examples

The CLI tool allows you to manage inventory from the terminal.

### Start the CLI
```bash
pipenv run python cli.py
```

### Menu Options
```
 My Inventory CLI Application 
Welcome! Let's manage our stock.

What would you like to do?
1. View all items
2. Add new item
3. Update item
4. Delete item
5. Search OpenFoodFacts
6. Add from OpenFoodFacts
7. Exit
```

### Example 1: View All Items
```
Enter your choice (1-7): 1

 Current Inventory
ID: 1 | Rice | Qty: 10 | Price: Ksh 200
ID: 2 | Sugar | Qty: 5 | Price: Ksh 150
```

### Example 2: Add New Item
```
Enter your choice (1-7): 2

 Add New Item 
Enter item name: Milk
Enter quantity: 12
Enter price (Ksh): 120
Successfully added Milk to inventory
```

### Example 3: Search OpenFoodFacts
```
Enter your choice (1-7): 5
Enter product name or barcode: nutella

Found: Nutella
Brand: Ferrero
Category: Spreads
```

### Example 4: Add from OpenFoodFacts
```
Enter your choice (1-7): 6
Enter product name or barcode: nutella
Enter quantity (default 1): 2
Added Nutella to inventory
```

### Example 5: Update Item
```
Enter your choice (1-7): 3

 Update Item 
Enter item ID to update: 1
Leave blank if you don't want to change a field.
New name (or press Enter to keep same): Brown Rice
New quantity (or press Enter to keep same): 15
New price (or press Enter to keep same): 250
Item updated successfully
```

### Example 6: Delete Item
```
Enter your choice (1-7): 4

 Delete Item 
Enter item ID to delete: 2
Are you sure you want to delete item 2? (yes/no): yes
Item deleted successfully
```

## Project Structure
```
inventory_project/
├── app.py                          # Main Flask application
├── cli.py                          # Command line interface
├── external_api.py                 # OpenFoodFacts API integration
├── Pipfile                         # Pipenv dependencies
├── Pipfile.lock                    # Locked dependencies
├── README.md                       # This file
├── templates/                      # HTML templates
│   ├── index.html                  # Main inventory UI
│   ├── login.html                  # Login page
│   └── register.html               # Register page
├── static/                         # Static assets
│   └── js/
│       ├── script.js               # Main UI JavaScript
│       └── auth.js                 # Authentication JavaScript
└── tests/                          # Test suite
    ├── test_app.py                 # API endpoint tests
    ├── test_cli.py                 # CLI command tests
    └── test_external_api.py        # External API tests
```

## Technologies Used
- Python 3.12 — Backend language
- Flask — Web framework
- Tailwind CSS — UI styling
- Requests — HTTP client for API calls
- Pipenv — Virtual environment management
- pytest — Testing framework
- unittest.mock — Mocking for tests

## Testing

Run the test suite:
```bash
pipenv run pytest tests/ -v
```

Check coverage:
```bash
pipenv run pytest tests/ --cov=app --cov=cli --cov=external_api
```

## Debug Tools
- Flask Debug Mode — Enabled with `app.run(debug=True)` for detailed error pages
- Postman — Use Postman to test API endpoints manually

## Author
Favour Kendi 

