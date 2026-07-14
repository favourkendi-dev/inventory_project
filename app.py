from flask import Flask, jsonify, request
from external_api import search_product_by_barcode, search_product_by_name

app = Flask(__name__)

# This is my mock database for now
inventory = []

@app.route('/')
def home():
    """Home route to check if the API is running"""
    return jsonify({"message": "Inventory Management System API is running!"})


# Have used GET so that i GET all items in inventory
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify({
        "success": True,
        "items": inventory,
        "total": len(inventory)
    })

# i used Add to Add a new item manually
@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({"success": False, "error": "Item name is required"}), 400
    
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

# My code for getting one specific item
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in inventory if item['id'] == item_id), None)
    if not item:
        return jsonify({"success": False, "error": f"Item with id {item_id} not found"}), 404
    return jsonify({"success": True, "item": item})

# I used Update to Update an existing item
@app.route('/items/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    item = next((item for item in inventory if item['id'] == item_id), None)
    if not item:
        return jsonify({"success": False, "error": f"Item with id {item_id} not found"}), 404
    
    data = request.get_json()
    if data.get('name'): item['name'] = data['name']
    if 'quantity' in data: item['quantity'] = data['quantity']
    if 'price' in data: item['price'] = data['price']
    if data.get('category'): item['category'] = data['category']
    
    return jsonify({"success": True, "message": f"Item updated successfully", "item": item})

# My code for deleting an item
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = next((item for item in inventory if item['id'] == item_id), None)
    if not item:
        return jsonify({"success": False, "error": f"Item with id {item_id} not found"}), 404
    inventory.remove(item)
    return jsonify({"success": True, "message": f"Item deleted successfully"})


# Tried Searching products from OpenFoodFacts
@app.route('/search', methods=['GET'])
def search_product():
    """Search product either by barcode or name"""
    query = request.args.get('q')
    barcode = request.args.get('barcode')
    
    if barcode:
        product = search_product_by_barcode(barcode)
    elif query:
        product = search_product_by_name(query)
    else:
        return jsonify({"success": False, "error": "Provide 'q' or 'barcode' parameter"}), 400
    
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
    return jsonify({"success": False, "error": "Product not found"}), 404

# Added product from external API to our inventory
@app.route('/items/from-external', methods=['POST'])
def add_from_external():
    """Add a product found on OpenFoodFacts directly into our inventory"""
    data = request.get_json()
    barcode = data.get('barcode')
    name = data.get('name')
    
    if not barcode and not name:
        return jsonify({"success": False, "error": "Barcode or name is required"}), 400
    
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

if __name__ == '__main__':
    app.run(debug=True)