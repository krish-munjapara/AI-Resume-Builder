import mysql.connector
from mysql.connector import Error


def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="resume_builder"
        )
        return conn
    except Error as e:
        print(f"Database Connection Error: {e}")
        return None


def save_student(name, email, phone, skills, education, projects, resume):

    conn = get_connection()

    if conn is None:
        print("Failed to connect to database.")
        return

    try:
        cursor = conn.cursor()

        query = """
        INSERT INTO students 
        (name, email, phone, skills, education, projects, resume)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (name, email, phone, skills, education, projects, resume)

        cursor.execute(query, values)
        conn.commit()

        print("Data saved successfully.")

    except Error as e:
        print(f"Database Insert Error: {e}")

    finally:
        cursor.close()
        conn.close()