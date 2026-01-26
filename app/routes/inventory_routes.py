from flask import Blueprint, request, jsonify
from app import db
from app.models.inventory import Inventory

inventory_bp = Blueprint("inventory_bp", __name__)

# ---------------------------
# GET ALL INVENTORY
# ---------------------------
@inventory_bp.route("/api/inventory", methods=["GET"])
def get_inventory():
    items = Inventory.query.all()
    return jsonify([{
        "id": i.id,
        "item_name": i.item_name,
        "qty": i.qty,
        "mrp": i.mrp
    } for i in items])

# ---------------------------
# CREATE OR UPDATE SINGLE ITEM
# ---------------------------
@inventory_bp.route("/api/inventory", methods=["POST"])
def add_inventory():
    data = request.get_json()
    if not data or not data.get("item_name"):
        return jsonify({"message": "Invalid payload"}), 400

    item_name = data["item_name"].strip()

    # Check if item already exists
    inventory = Inventory.query.filter_by(item_name=item_name).first()
    if inventory:
        # Update existing item
        inventory.qty = data.get("qty", inventory.qty)
        inventory.mrp = data.get("mrp", inventory.mrp)
    else:
        # Create new item
        inventory = Inventory(
            item_name=item_name,
            qty=data.get("qty", 0),
            mrp=data.get("mrp", 0)
        )
        db.session.add(inventory)

    try:
        db.session.commit()
        return jsonify({
            "message": "Inventory saved successfully",
            "item": {
                "id": inventory.id,
                "item_name": inventory.item_name,
                "qty": inventory.qty,
                "mrp": inventory.mrp
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# ---------------------------
# BULK INVENTORY SAVE / UPDATE
# ---------------------------
@inventory_bp.route("/api/inventory/bulk", methods=["POST"])
def bulk_inventory_upload():
    data = request.get_json()
    if not data or "items" not in data:
        return jsonify({"message": "Invalid payload"}), 400

    items = data["items"]
    if not items:
        return jsonify({"message": "No items to save"}), 400

    for item in items:
        if not item.get("item_name"):
            continue

        item_name = item["item_name"].strip()
        existing = Inventory.query.filter_by(item_name=item_name).first()
        if existing:
            # If exists, add quantity and update MRP if provided
            existing.qty += item.get("qty", 0)
            if item.get("mrp") is not None:
                existing.mrp = item["mrp"]
        else:
            # Create new inventory record
            new_item = Inventory(
                item_name=item_name,
                qty=item.get("qty", 0),
                mrp=item.get("mrp", 0)
            )
            db.session.add(new_item)

    try:
        db.session.commit()
        return jsonify({"message": "Inventory bulk saved/updated successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# ---------------------------
# UPDATE SINGLE ITEM
# ---------------------------
@inventory_bp.route("/api/inventory/<int:item_id>", methods=["PUT"])
def update_inventory(item_id):
    data = request.get_json()
    inventory = Inventory.query.get(item_id)
    if not inventory:
        return jsonify({"message": "Item not found"}), 404

    inventory.item_name = data.get("item_name", inventory.item_name)
    inventory.qty = data.get("qty", inventory.qty)
    inventory.mrp = data.get("mrp", inventory.mrp)

    try:
        db.session.commit()
        return jsonify({"message": "Inventory updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# ---------------------------
# DELETE SINGLE ITEM
# ---------------------------
@inventory_bp.route("/api/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory(item_id):
    inventory = Inventory.query.get(item_id)
    if not inventory:
        return jsonify({"message": "Item not found"}), 404

    try:
        db.session.delete(inventory)
        db.session.commit()
        return jsonify({"message": "Inventory deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500
