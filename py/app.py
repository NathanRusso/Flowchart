"""
This file will contain the logic to get data from the course database.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import mariadb
import sys
import os

############################## Global Variables ##############################


course_query = (
    "SELECT c.quarter, d.code, c.course, c.credits, c.title, c.description "
    "FROM courses c JOIN departments d ON c.department = d.id "
    "WHERE d.code = ? AND c.course = ? ORDER BY c.quarter DESC LIMIT 1"
)
connection = None
cursor = None

app = Flask(__name__)   # Setup flask app
CORS(app)

load_dotenv()           # Load Environment variables


############################## Functions ##############################


def connect_to_database():
    """
    Tries to connect to the course information database.
    """
    try:
        global connection, cursor
        connection = mariadb.connect(
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            host=os.getenv("DATABASE_HOST"),
            port=3306,
            database=os.getenv("DATABASE_NAME")
        )
        cursor = connection.cursor(dictionary=True)
        print(f"[SUCCESS] connect_to_database(): Connected to course database!")
    except Exception as e:
        print(f"[ERROR] connect_to_database(): Could not connect to course database: {e}!")
        sys.exit(1)


def disconnect_from_database():
    """
    Tries to disconnect from the course information database.
    """
    try:
        cursor.close()
        connection.close()
        print(f"[SUCCESS] disconnect_from_database(): Disconnected from the course database!")
    except Exception as e:
        print(f"[ERROR] disconnect_from_database(): Could not disconnect from the course database: {e}!")


@app.route("/course", methods=["GET"])
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
        if connection is None or cursor is None: raise AttributeError("Database connection has not established")

        discipline = request.args.get('discipline')
        number = request.args.get('number')
        cursor.execute(course_query, (discipline, number))
        courseInformation = cursor.fetchone()
        #print(courseInformation)

        if courseInformation is None: raise ValueError(f"Could not find class information matching {discipline}-{number}")

        return jsonify(courseInformation), 200
    except (AttributeError, ValueError) as ce:      # custom exception
        exception_message = f"[ERROR] get_course_information(): {ce}!"
        print(exception_message)
        return jsonify(exception_message), 500
    except Exception as e:
        exception_message = f"[ERROR] get_course_information(): Could not get course information: {e}!"
        print(exception_message)
        return jsonify(exception_message), 500
   

if __name__ == "__main__":
    connect_to_database()       # Connect to the course information database
    app.run(port=5000, debug=True)
