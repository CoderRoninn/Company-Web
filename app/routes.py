# Handles incoming requests and calls the appropriate services.

from flask import Blueprint, request, jsonify
from app.database import add_user, get_all_users, update_user_status

# All routes in this file are grouped under "main_bp"
main_bp = Blueprint("main", __name__)

VALID_STATUSES = ("New", "InProgress", "Done")


@main_bp.route("/api/submit", methods=["POST"])
def submit_form():
    """Receives the contact form data from the Wix site and saves it."""
    try:
        data = request.get_json()

        name = data.get("name", "")
        email = data.get("email", "")
        phone = data.get("phone", "")
        service = data.get("service", "")
        message = data.get("message", "")

        if not name or not email:
            return jsonify({"success": False, "error": "Name and email are required"}), 400

        saved = add_user(name, email, phone, service, message)

        if saved:
            return jsonify({"success": True}), 201
        else:
            return jsonify({"success": False, "error": "Could not save to database"}), 500

    except Exception as e:
        print(f"[routes] Failed to handle form submission: {e}")
        return jsonify({"success": False, "error": "Something went wrong"}), 500


@main_bp.route("/api/users", methods=["GET"])
def list_users():
    """Returns all saved users as JSON. Used by the dashboard page on Wix."""
    try:
        users = get_all_users()
        return jsonify({"success": True, "users": users}), 200
    except Exception as e:
        print(f"[routes] Failed to fetch users: {e}")
        return jsonify({"success": False, "error": "Something went wrong"}), 500


@main_bp.route("/api/users/<int:user_id>/status", methods=["POST"])
def change_status(user_id):
    """Updates a user's status (New / InProgress / Done). Used by the dashboard."""
    try:
        data = request.get_json()
        new_status = data.get("status", "")

        if new_status not in VALID_STATUSES:
            return jsonify({"success": False, "error": "Invalid status"}), 400

        updated = update_user_status(user_id, new_status)

        if updated:
            return jsonify({"success": True}), 200
        else:
            return jsonify({"success": False, "error": "Could not update status"}), 500

    except Exception as e:
        print(f"[routes] Failed to update status: {e}")
        return jsonify({"success": False, "error": "Something went wrong"}), 500
