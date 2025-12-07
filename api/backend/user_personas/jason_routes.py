from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

jason = Blueprint("jason", __name__)

    
#Addressed in ui
@jason.route("/regions/status/<string:status>", methods=["GET"])
def get_regions_by_status(status):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM Region WHERE Status = %s AND AdminID = %s", (status, 'admin_jason_001'))
        regions = cursor.fetchall()
        cursor.close()
        if not regions:
            return jsonify({"error": f"No regions found with status '{status}'"}), 404
        return jsonify(regions), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    

#Addressed in ui
@jason.route("/fetch_activity/<string:user_id>", methods=["GET"])
def fetch_activity(user_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("""
            SELECT 
                input.InputID,
                TIME_FORMAT(input.Time, '%%H:%%i:%%s') as InputTime,
                input.Content as InputContent,
                input.RegionID,
                output.OutputID,
                output.OutputData,
                TIME_FORMAT(output.Timestamp, '%%H:%%i:%%s') as OutputTime
            FROM Input input
            LEFT JOIN Output output ON input.InputID = output.InputID
            WHERE input.UserID = %s
            ORDER BY input.Time DESC
        """, (user_id,))
        
        activity = cursor.fetchall()
        cursor.close()

        if not activity:
            return jsonify({"error": f"No inputs or outputs found for user '{user_id}'"}), 404

        return jsonify(activity), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
#Addressed in ui
#To clarify because this one is a little goofy, it would force all cached responses to be deleted in the event of a critical issue with the LLM. 
@jason.route("/nuclear-button", methods=["DELETE"])
def nuclear_button():
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT COUNT(*) as count FROM Output")
        result = cursor.fetchone()
        deleted_count = result["count"] if result else 0
        cursor.execute("DELETE FROM Output")
        db.get_db().commit()
        cursor.close()

        return jsonify({
            "message": "Nuclear button pressed, clanker outputs destroyed",
            "status": "All outputs are donezo",
            "outputs_destroyed": deleted_count
        }), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
#ui
@jason.route("/users_delete/<string:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM User WHERE UserID = %s", (user_id,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": f"User {user_id} not found"}), 404
        
        cursor.execute("DELETE FROM User WHERE UserID = %s", (user_id,))
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": f"User {user_id} deleted successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    


#In ui
@jason.route("/regions/<string:region_id>/status", methods=["PUT"])
def update_region_status(region_id):
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data"}), 400
        
        status = data.get('status')
        
        if not status:
            return jsonify({"error": "You need a status"}), 400
        
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT RegionID FROM Region WHERE RegionID = %s", (region_id,))
        if not cursor.fetchone():
            cursor.close()
            return jsonify({"error": "Region not found"}), 404
        
        cursor.execute("UPDATE Region SET Status = %s WHERE RegionID = %s", (status, region_id))
        db.get_db().commit()
        cursor.close()
        
        return jsonify({"message": "Region status change worked!"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500



