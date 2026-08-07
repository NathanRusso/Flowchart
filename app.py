"""
This file contains the logic to get data from the course database.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import mariadb
import os


COURSE_QUERY = (
    "SELECT c.quarter, d.code, c.course, c.credits, c.title, c.description "
    "FROM courses c JOIN departments d ON c.department = d.id "
    "WHERE d.code = ? AND c.course = ? ORDER BY c.quarter DESC LIMIT 1"
)
pool = None
connection = None
cursor = None

# Startup code
app = Flask(__name__)   # Setup flask app
CORS(app)               # Handle requests
load_dotenv()           # Load Environment variables


def connect_to_database():
    """
    Tries to connect to the course information database.
    """
    try:
        global pool, connection, cursor
        pool = mariadb.ConnectionPool(
            pool_name="flowchart_pool",
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            host=os.getenv("DATABASE_HOST"),
            port=3306,
            database=os.getenv("DATABASE_NAME")
        )
        connection = pool.get_connection()
        cursor = connection.cursor(dictionary=True)
        print(f"[SUCCESS] connect_to_database(): Connected to course database!")
    except Exception as e:
        print(f"[ERROR] connect_to_database(): Could not connect to course database: {e}!")


def disconnect_from_database():
    """
    Tries to disconnect from the course information database.
    """
    try:
        cursor.close()
        connection.close()
        pool.close()
        print(f"[SUCCESS] disconnect_from_database(): Disconnected from the course database!")
    except Exception as e:
        print(f"[ERROR] disconnect_from_database(): Could not disconnect from the course database: {e}!")


# Startup (continue)
connect_to_database()   # Connection to the course information database


@app.route("/api/course", methods=["GET"])
def get_course_information() -> jsonify:
    """
    This gets the most recent course information for the selected course.

    Args:
        discipline (str): The course discipline. Ex: ABCD.
        number (str): The course number. Ex: 999.

    Returns:
        jsonify: The course's information.
    """
    try:
        if connection is None or cursor is None: connect_to_database()  # Try to reconnect once
        if connection is None or cursor is None: raise AttributeError("Database connection has not established")

        discipline = request.args.get('discipline')
        number = request.args.get('number')
        cursor.execute(COURSE_QUERY, (discipline, number))
        courseInformation = cursor.fetchone()
        if courseInformation is None: raise ValueError(f"Could not find class information matching {discipline}-{number}")

        return jsonify(courseInformation), 200      # Ok
    except AttributeError as ae:
        exception_message = f"[ERROR] get_course_information(): {ae}!"
        print(exception_message)
        return jsonify(exception_message), 503      # Service Unavailable
    except ValueError as ve:
        exception_message = f"[ERROR] get_course_information(): {ve}!"
        print(exception_message)
        return jsonify(exception_message), 404      # Not Found
    except Exception as e:
        exception_message = f"[ERROR] get_course_information(): Could not get course information: {e}!"
        print(exception_message)
        return jsonify(exception_message), 500      # Internal Server Error


if __name__ == "__main__":
    connect_to_database()                           # Connect to the course information database
    app.run(host="0.0.0.0", port=5000, debug=True)  # Development server only
