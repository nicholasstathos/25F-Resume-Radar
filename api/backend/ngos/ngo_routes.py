from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# BluePrint for the new grad persona 
ngos = Blueprint("ngos", __name__)


# Get all NGOs with optional filtering by country, focus area, and founding year
# Example: /ngo/ngos?country=United%20States&focus_area=Environmental%20Conservation
@ngos.route("/users", methods=["GET"])
def get_all_users():
    try:
        current_app.logger.info('Getting all users request')
        cursor = db.get_db().cursor()

        # Note: Query parameters are added after the main part of the URL.
        # Here is an example:
        # http://localhost:4000/ngo/ngos?founding_year=1971
        # founding_year is the query param.

        # Get query parameters for filtering

        # Prepare the Base query
        query = "SELECT * FROM User"
        params = []
        filters = []

        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query, params)
        ngos = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f'Successfully retrieved {len(ngos)} NGOs')
        return jsonify(ngos), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_ngos: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Get detailed information about a specific NGO including its projects and donors
# Example: /ngo/ngos/1
@ngos.route("/users/<int:user_id>", methods=["GET"])
def get_ngo(user_id):
    try:
        cursor = db.get_db().cursor()

        # Get NGO details
        cursor.execute("SELECT * FROM User WHERE UserID = %s", (user_id,))
        ngo = cursor.fetchone()

        if not ngo:
            return jsonify({"error": "NGO not found"}), 404

        cursor.close()
        return jsonify(ngo), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Create a new NGO
# Required fields: Name, Country, Founding_Year, Focus_Area, Website
# Example: POST /ngo/ngos with JSON body
@ngos.route("/feedback/<int:user_id>", methods=["GET"])
def get_feedback(user_id):
    try:

        cursor = db.get_db().cursor()

        # Get NGO details
        cursor.execute("SELECT * FROM Feedback WHERE UserID = %s", (user_id))

        feedback = cursor.fetchall()

        return (
            jsonify(feedback),
            200,
        )
    except Error as e:
        return jsonify({"error": str(e)}), 500
    

# Create a new NGO
# Required fields: Name, Country, Founding_Year, Focus_Area, Website
# Example: POST /ngo/ngos with JSON body
@ngos.route("/jobs/<string:keyword>", methods=["GET"])
def get_jobs_by_keyword(keyword):
    try:
        cursor = db.get_db().cursor()

        # Get jobs by keyword
        cursor.execute("SELECT * FROM Job WHERE Title LIKE '%{}%' OR Company LIKE '%{}%';".format(keyword, keyword))

        feedback = cursor.fetchall()

        return (
            jsonify(feedback),
            200,
        )
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Update an existing NGO's information
# Can update any field except NGO_ID
# Example: PUT /ngo/ngos/1 with JSON body containing fields to update
@ngos.route("/ngos/<int:ngo_id>", methods=["PUT"])
def update_ngo(ngo_id):
    try:
        data = request.get_json()

        # Check if NGO exists
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM WorldNGOs WHERE NGO_ID = %s", (ngo_id,))
        if not cursor.fetchone():
            return jsonify({"error": "NGO not found"}), 404

        # Build update query dynamically based on provided fields
        update_fields = []
        params = []
        allowed_fields = ["Name", "Country", "Founding_Year", "Focus_Area", "Website"]

        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(ngo_id)
        query = f"UPDATE WorldNGOs SET {', '.join(update_fields)} WHERE NGO_ID = %s"

        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "NGO updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get all projects associated with a specific NGO
# Example: /ngo/ngos/1/projects
@ngos.route("/ngos/<int:ngo_id>/projects", methods=["GET"])
def get_ngo_projects(ngo_id):
    try:
        cursor = db.get_db().cursor()

        # Check if NGO exists
        cursor.execute("SELECT * FROM WorldNGOs WHERE NGO_ID = %s", (ngo_id,))
        if not cursor.fetchone():
            return jsonify({"error": "NGO not found"}), 404

        # Get all projects for the NGO
        cursor.execute("SELECT * FROM Projects WHERE NGO_ID = %s", (ngo_id,))
        projects = cursor.fetchall()
        cursor.close()

        return jsonify(projects), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    

# Create a new NGO
# Required fields: Name, Country, Founding_Year, Focus_Area, Website
# Example: POST /ngo/ngos with JSON body
@ngos.route("/jobs/<int:JobID>, <int:ResumeID>", methods=["GET"])
def get_match_score(keyword):
    try:
        cursor = db.get_db().cursor()

        # Get jobs by keyword
        cursor.execute("SELECT * FROM Job WHERE Title LIKE '%{}%' OR Company LIKE '%{}%';".format(keyword, keyword))

        feedback = cursor.fetchall()

        return (
            jsonify(feedback),
            200,
        )
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get all donors associated with a specific NGO
# Example: /ngo/ngos/1/donors
@ngos.route("/ngos/<int:ngo_id>/donors", methods=["GET"])
def get_ngo_donors(ngo_id):
    try:
        cursor = db.get_db().cursor()

        # Check if NGO exists
        cursor.execute("SELECT * FROM WorldNGOs WHERE NGO_ID = %s", (ngo_id,))
        if not cursor.fetchone():
            return jsonify({"error": "NGO not found"}), 404

        # Get all donors for the NGO
        cursor.execute("SELECT * FROM Donors WHERE NGO_ID = %s", (ngo_id,))
        donors = cursor.fetchall()
        cursor.close()

        return jsonify(donors), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
