from flask import Flask, jsonify, request
from datetime import datetime
import pytz
import uuid

app = Flask("Notes")
storage = []

@app.route("/", methods=["GET"])
def get_hi():
    return "Hii", 200

@app.route("/items", methods=["GET"])
def get_item():
    return jsonify(storage), 200

@app.route("/items", methods=["POST"])
def add_items():
    item = request.json
    try:
        if "title" not in item.keys() or "body" not in item.keys():
            return jsonify({"error": "Keys don't exist"}), 400
        
        if not isinstance(item["title"], str) or not isinstance(item["body"], str):
            return jsonify({"error": "Datatype is not String"}), 400
        
        if item["title"] == "":
            return jsonify({"error": "Title cannot be empty"}), 400
        
        new_data = {
            "title": item["title"],
            "body": item["body"],
            "timestamp": datetime.now(pytz.utc).strftime('%Y-%m-%d %H:%M:%S'),
            "_id": str(uuid.uuid4())
        }
        
        storage.append(new_data)
        return jsonify(new_data), 201
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@app.route("/items", methods=["DELETE"])
def delete_items(item_id):
    item_id=request.args.get("item_id")
    # Search for the item with the matching _id
    for index, item in enumerate(storage):
        if item["_id"] == item_id:
            deleted_item = storage.pop(index)
            return jsonify(deleted_item), 200
    
    return jsonify({"error": "Item not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
