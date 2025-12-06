from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# BluePrint for the sarah persona (job matching)
sarah = Blueprint("sarah", __name__)


# ex: /sarah/jobs
@sarah.route("/jobs", methods=["GET"])
def get_all_jobs():
    try:
        current_app.logger.info('Getting all jobs request')
        cursor = db.get_db().cursor()

        query = "SELECT * FROM Job"
        params = []

        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query, params)
        jobs = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f'Successfully retrieved {len(jobs)} jobs')
        return jsonify(jobs), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_jobs: {str(e)}')
        return jsonify({"error": str(e)}), 500


# ex: /sarah/jobs/job_001
@sarah.route("/jobs/<string:job_id>", methods=["GET"])
def get_job(job_id):
    try:
        cursor = db.get_db().cursor()

        # Get job details
        cursor.execute("SELECT * FROM Job WHERE JobID = %s", (job_id,))
        job = cursor.fetchone()

        if not job:
            return jsonify({"error": "Job not found"}), 404

        cursor.close()
        return jsonify(job), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# ex: /sarah/jobs/search/Engineer
@sarah.route("/jobs/search/<string:keyword>", methods=["GET"])
def get_jobs_by_keyword(keyword):
    try:
        cursor = db.get_db().cursor()

        cursor.execute("""
            SELECT j.*, AVG(r.ResumeScore) as avg_resume_score
            FROM Job j
            LEFT JOIN Resume r ON j.JobID = r.JobID
            WHERE j.Title LIKE %s OR j.Company LIKE %s
            GROUP BY j.JobID
        """, (f"%{keyword}%", f"%{keyword}%"))

        jobs = cursor.fetchall()
        cursor.close()

        return jsonify(jobs), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


@sarah.route("/users/<string:user_id>", methods=["GET"])
def get_user_email_and_resume(user_id):
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT Email FROM User WHERE UserID = %s", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        email = user["Email"]

        cursor.execute("""
            SELECT resume.ResumeID, resume.ResumeScore, resume.VersionNum
            FROM Resume resume
            JOIN Job job ON resume.JobID = job.JobID
            WHERE job.UserID = %s
        """, (user_id,))
        resumes = cursor.fetchall()

        cursor.close()
        
        response = {
            "user_id": user_id,
            "email": email,
            "resumes": [
                {
                    "resume_id": resume["ResumeID"],
                    "resume_score": resume["ResumeScore"],
                    "version_num": resume["VersionNum"]
                }
                for resume in resumes
            ]
        }
        
        return jsonify(response), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    

@sarah.route("/resume", methods=["GET"])
def get_all_resumes():
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM Resume LIMIT 1")
        resumes = cursor.fetchall()
        cursor.close()
        return jsonify(resumes), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
@sarah.route("/users/<string:user_id>", methods=["PUT"])
def update_user_profile(user_id):
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        name = data.get('name')
        email = data.get('email')
        if not name or not email:
            return jsonify({"error": "Name and email are required"}), 400
        
        cursor = db.get_db().cursor()
        cursor.execute("SELECT UserID FROM User WHERE UserID = %s", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            cursor.close()
            return jsonify({"error": "User not found"}), 404
        cursor.execute("SELECT UserID FROM User WHERE Email = %s AND UserID != %s", (email, user_id))
        existing = cursor.fetchone()
        
        if existing:
            cursor.close()
            return jsonify({"error": "Email already in use"}), 409
        cursor.execute("""
            UPDATE User 
            SET Name = %s, Email = %s
            WHERE UserID = %s
        """, (name, email, user_id))
        
        db.get_db().commit()
        cursor.close()
        
        return jsonify({"message": "User profile updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    

@sarah.route("/documents", methods=["POST"])
def create_document():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        doc_id = data.get('doc_id')
        linkedin_url = data.get('linkedin_url')
        contents = data.get('contents')
        user_id = data.get('user_id')
        
        if not doc_id:
            return jsonify({"error": "Document ID is required"}), 400
        
        cursor = db.get_db().cursor()
        
        cursor.execute("""
            INSERT INTO Document (DocID, LinkedinURL, Contents, UserID)
            VALUES (%s, %s, %s, %s)
        """, (doc_id, linkedin_url, contents, user_id))
        
        db.get_db().commit()
        cursor.close()
        
        return jsonify({"message": "Document created successfully", "doc_id": doc_id}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500