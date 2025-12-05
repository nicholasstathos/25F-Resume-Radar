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
    
