from flask import Flask, jsonify, request

app = Flask(__name__)

# Mock Database
inventory = []

@app.route('/')
def home():
    return jsonify({"message": "Inventory Management System API is running!"})

# GET all items
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify({
        "success": True,
        "items": inventory,
        "total": len(inventory)
    })

# POST for Add new item
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
        "category": data.get('category', 'General')
    }
    
    inventory.append(new_item)
    
    return jsonify({
        "success": True,
        "message": f"Successfully added {new_item['name']} to inventory",
        "item": new_item
    }), 201

# GET single item by ID
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in inventory if item['id'] == item_id), None)
    
    if not item:
        return jsonify({
            "success": False,
            "error": f"Item with id {item_id} not found"
        }), 404
    
    return jsonify({
        "success": True,
        "item": item
    })

# PATCH for  Updating an item
@app.route('/items/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    item = next((item for item in inventory if item['id'] == item_id), None)
    
    if not item:
        return jsonify({
            "success": False,
            "error": f"Item with id {item_id} not found"
        }), 404
    
    data = request.get_json()
    
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
        "message": f"Item '{item['name']}' updated successfully",
        "item": item
    })

# DELETE an item
@app.route('/items/<int:item_id>', methods=['DELETE'])
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
        "message": f"Item '{item['name']}' has been deleted successfully"
    })

if __name__ == '__main__':
    app.run(debug=True)