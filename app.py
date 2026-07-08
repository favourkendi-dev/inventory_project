# POST - Add new item
@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({"success": False, "error": "Item name is required"}), 400
    
    # Create new item
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