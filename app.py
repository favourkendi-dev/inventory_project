from flask import Flask, jsonify, request, render_template, session
from functools import wraps
from external_api import search_product_by_barcode, search_product_by_name

app = Flask(__name__)
app.secret_key = 'my_secret_key_for_sessions'

# My mock database for storing inventory items
inventory = []

# My mock database for storing users (plain text for demo)
users = []


# My decorator to check if user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({
                "success": False,
                "error": "Please login to access this resource"
            }), 401
        return f(*args, **kwargs)
    return decorated_function


# Route to serve the main HTML page
@app.route('/')
def index():
    return render_template('index.html')


# API route to check if backend is running
@app.route('/api')
def api_home():
    return jsonify({"message": "Inventory Management System API is running!"})


# My route to check if user is logged in
@app.route('/check-session', methods=['GET'])
def check_session():
    if 'user_id' in session:
        return jsonify({
            "success": True,
            "logged_in": True,
            "user": {
                "id": session['user_id'],
                "username": session['username']
            }
        })
    return jsonify({
        "success": True,
        "logged_in": False
    })


# My route to render login page
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


# My route to render register page
@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')


# My route to handle user registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({
            "success": False,
            "error": "Username and password are required"
        }), 400
    
    username = data['username']
    password = data['password']
    
    # Check if user already exists
    existing_user = next((user for user in users if user['username'] == username), None)
    if existing_user:
        return jsonify({
            "success": False,
            "error": "Username already exists"
        }), 400
    
    # Create new user
    new_user = {
        "id": len(users) + 1,
        "username": username,
        "password": password
    }
    users.append(new_user)
    
    return jsonify({
        "success": True,
        "message": "Registration successful! Please login."
    }), 201


# My route to handle user login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({
            "success": False,
            "error": "Username and password are required"
        }), 400
    
    username = data['username']
    password = data['password']
    
    # Find user by username
    user = next((user for user in users if user['username'] == username), None)
    
    if not user:
        return jsonify({
            "success": False,
            "error": "User not found"
        }), 404
    
    # Check password (plain text comparison)
    if user['password'] != password:
        return jsonify({
            "success": False,
            "error": "Incorrect password"
        }), 401
    
    # Store user in session
    session['user_id'] = user['id']
    session['username'] = user['username']
    
    return jsonify({
        "success": True,
        "message": f"Welcome back, {username}!",
        "user": {
            "id": user['id'],
            "username": user['username']
        }
    })


# My route to handle user logout
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({
        "success": True,
        "message": "Logged out successfully"
    })


# My route to get all items in inventory
@app.route('/items', methods=['GET'])
@login_required
def get_items():
    return jsonify({
        "success": True,
        "items": inventory,
        "total": len(inventory)
    })


# My route to add a new item manually
@app.route('/items', methods=['POST'])
@login_required
def add_item():
    data = request.get_json()
    
    # This one will Check if item name is provided
    if not data or not data.get('name'):
        return jsonify({
            "success": False, 
            "error": "Item name is required"
        }), 400
    
    # Creates the new item
    new_item = {
        "id": len(inventory) + 1,
        "name": data['name'],
        "quantity": data.get('quantity', 0),
        "price": data.get('price', 0.0),
        "category": data.get('category', 'General'),
        "barcode": data.get('barcode')
    }
    
    inventory.append(new_item)
    
    return jsonify({
        "success": True,
        "message": f"Successfully added {new_item['name']} to inventory",
        "item": new_item
    }), 201


# My route to get a single item by ID
@app.route('/items/<int:item_id>', methods=['GET'])
@login_required
def get_item(item_id):
    item = next((item for item in inventory if item['id'] == item_id), None)
    
    if not item:
        return jsonify({
            "success": False, 
            "error": f"Item with id {item_id} not found"
        }), 404
    
    return jsonify({"success": True, "item": item})


# My route to update an existing item
@app.route('/items/<int:item_id>', methods=['PATCH'])
@login_required
def update_item(item_id):
    item = next((item for item in inventory if item['id'] == item_id), None)
    
    if not item:
        return jsonify({
            "success": False, 
            "error": f"Item with id {item_id} not found"
        }), 404
    
    data = request.get_json()
    
    # Update only the fields that are provided
    if data.get('name'):
        item['name'] = data['name']
    if 'quantity' in data:
        item['quantity'] = data['quantity']
    if 'price' in data:
        item['price'] = data['price']
    if data.get('category'):
        item['category'] = data['category']
    
    return jsonify({
        "success": True, 
        "message": "Item updated successfully", 
        "item": item
    })


# My route to delete an item
@app.route('/items/<int:item_id>', methods=['DELETE'])
@login_required
def delete_item(item_id):
    item = next((item for item in inventory if item['id'] == item_id), None)
    
    if not item:
        return jsonify({
            "success": False, 
            "error": f"Item with id {item_id} not found"
        }), 404
    
    inventory.remove(item)
    
    return jsonify({
        "success": True, 
        "message": "Item deleted successfully"
    })


# My route to search products from OpenFoodFacts
@app.route('/search', methods=['GET'])
@login_required
def search_product():
    query = request.args.get('q')
    barcode = request.args.get('barcode')
    
    # Searching by barcode or name
    if barcode:
        product = search_product_by_barcode(barcode)
    elif query:
        product = search_product_by_name(query)
    else:
        return jsonify({
            "success": False, 
            "error": "Provide 'q' or 'barcode' parameter"
        }), 400
    
    # Returning  product if found
    if product:
        return jsonify({
            "success": True,
            "product": {
                "name": product.get('product_name'),
                "brand": product.get('brands'),
                "category": product.get('categories'),
                "barcode": product.get('code'),
                "nutrition": product.get('nutriments', {})
            }
        })
    
    return jsonify({
        "success": False, 
        "error": "Product not found"
    }), 404


# My route to add a product from OpenFoodFacts to inventory
@app.route('/items/from-external', methods=['POST'])
@login_required
def add_from_external():
    data = request.get_json()
    barcode = data.get('barcode')
    name = data.get('name')
    
    # Need at least barcode or name
    if not barcode and not name:
        return jsonify({
            "success": False, 
            "error": "Barcode or name is required"
        }), 400
    
    # Try to get real data from OpenFoodFacts
    product = None
    if barcode:
        product = search_product_by_barcode(barcode)
    elif name:
        product = search_product_by_name(name)
    
    # Fallback if API fails or product not found
    if not product:
        print("Using mock product data - API unavailable")
        product = {
            "product_name": name or "Unknown Product",
            "brands": "Generic",
            "categories": "General",
            "code": barcode or "Unknown"
        }
    
    # Create new item from external data
    new_item = {
        "id": len(inventory) + 1,
        "name": product.get('product_name', name or 'Unknown Product'),
        "quantity": data.get('quantity', 1),
        "price": data.get('price', 0.0),
        "category": product.get('categories', 'General'),
        "barcode": barcode or product.get('code'),
        "brand": product.get('brands', 'Unknown')
    }
    
    inventory.append(new_item)
    
    return jsonify({
        "success": True,
        "message": f"Added {new_item['name']} to inventory",
        "item": new_item,
        "note": "Used mock data (API unavailable)" if not product.get('product_name') else "From OpenFoodFacts"
    }), 201


# Running  the app
if __name__ == '__main__':
    app.run(debug=True)