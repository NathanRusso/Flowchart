"""
This file will contain the logic to get data from the course database.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import mariadb
import sys
import os

course_query = (
    "SELECT c.quarter, d.code, c.course, c.credits, c.title, c.description "
    "FROM courses c JOIN departments d ON c.department = d.id "
    "WHERE d.code = ? AND c.course = ? ORDER BY c.quarter DESC LIMIT 1"
)

# Load Environment variables
load_dotenv()

# Setup flask app
app = Flask(__name__)
CORS(app)


@app.route("/course", methods=["GET"])
def getCourseInformation() -> jsonify:
    """
    This gets the most recent course information for the selected course.

    Args:
        discipline (str): The course discipline. Ex: ABCD.
        number (str): The course number. Ex: 999.

    Returns:
        jsonify: The course's information.
    """


    try:
        # Connect to the database
        #try:
        connection = mariadb.connect(
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            host=os.getenv("DATABASE_HOST"),
            port=3306,
            database=os.getenv("DATABASE_NAME")
        )
        cursor = connection.cursor(dictionary=True)
        print(f"[SUCCESS] Connected to MySQL MariaDB database!")
        #except Exception as e:
        #    print(f"[ERROR] Could not connect to MySQL MariaDB database: {e}!")
        #    sys.exit(1)

        discipline = request.args.get('discipline')
        number = request.args.get('number')
        cursor.execute(course_query, (discipline, number))
        courseInformation = cursor.fetchone()
        print(courseInformation)
        cursor.close()
        connection.close()
        return jsonify(courseInformation), 200
    except Exception as e:
        print(f"[ERROR] getCourseInformation(): Could not get course information:: {e}!")
        cursor.close()
        connection.close()
        return jsonify(f"[ERROR] getCourseInformation(): Could not get course information:: {e}!"), 500

#getCourseInformation("CSCI", "320")

#cursor.close()

if __name__ == "__main__":
    app.run(port=5000, debug=True)