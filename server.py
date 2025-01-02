from flask import Flask, jsonify, request
from datetime import datetime
import pytz
import uuid

app = Flask("Notes")
storage = []

@app.route("/", methods=["GET"])
def get_hi():
    return "Hii", 200

@app.route("/posts", methods=["GET"])
def get_item():
    return jsonify(storage), 200

@app.route("/add", methods=["POST"])
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

@app.route("/delete", methods=["DELETE"])
def delete_items():
    item_id=request.args.get("item_id")
    # Search for the item with the matching _id
    for index, item in enumerate(storage):
        if item["_id"] == item_id:
            deleted_item = storage.pop(index)
            return jsonify(deleted_item), 200
    
    return jsonify({"error": "Item not found"}), 404

@app.route("/edit", methods=["PUT"])
def edit_item():
    item_id=request.args.get("item_id")
    new_item = request.json
    
    try:
        if "title" not in new_item.keys() or "body" not in new_item.keys():
            return jsonify({"error": "Keys don't exist"}), 400
        
        if not isinstance(new_item["title"], str) or not isinstance(new_item["body"], str):
            return jsonify({"error": "Datatype is not String"}), 400
        
        if new_item["title"] == "":
            return jsonify({"error": "Title cannot be empty"}), 400
        
        for index, item in enumerate(storage):
            if item["_id"] == item_id:
                storage[index]["title"]=new_item["title"]
                storage[index]["body"]=new_item["body"]
                storage[index]["timestamp"]=datetime.now(pytz.utc).strftime('%Y-%m-%d %H:%M:%S')        
            return jsonify(storage[index]), 200
        return jsonify({"error": "ID Not found !!", "message": str(e)}), 500
        
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True)
