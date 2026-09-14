from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)


# ==========================================
# MYSQL DATABASE CONNECTION
# ==========================================
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="bookstore_db"
    )

    return connection


# ==========================================
# HOME
# ==========================================
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Bookstore REST API is running"
    }), 200


# ==========================================
# GET ALL BOOKS
# ==========================================
@app.route("/books", methods=["GET"])
def get_books():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM books")

    books = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(books), 200


# ==========================================
# GET ONE BOOK
# ==========================================
@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM books WHERE id = %s",
        (book_id,)
    )

    book = cursor.fetchone()

    cursor.close()
    connection.close()

    if book is None:
        return jsonify({
            "error": "Book not found"
        }), 404

    return jsonify(book), 200


# ==========================================
# CREATE BOOK
# ==========================================
@app.route("/books", methods=["POST"])
def add_book():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON body is required"
        }), 400

    title = data.get("title")
    author = data.get("author")

    if not title or not author:
        return jsonify({
            "error": "Title and author are required"
        }), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    sql = """
        INSERT INTO books (title, author)
        VALUES (%s, %s)
    """

    cursor.execute(sql, (title, author))

    connection.commit()

    new_book_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Book created successfully",
        "id": new_book_id,
        "title": title,
        "author": author
    }), 201


# ==========================================
# UPDATE BOOK
# ==========================================
@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON body is required"
        }), 400

    title = data.get("title")
    author = data.get("author")

    if not title or not author:
        return jsonify({
            "error": "Title and author are required"
        }), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    # Check if book exists
    cursor.execute(
        "SELECT id FROM books WHERE id = %s",
        (book_id,)
    )

    book = cursor.fetchone()

    if book is None:
        cursor.close()
        connection.close()

        return jsonify({
            "error": "Book not found"
        }), 404

    # Update book
    sql = """
        UPDATE books
        SET title = %s, author = %s
        WHERE id = %s
    """

    cursor.execute(sql, (title, author, book_id))

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Book updated successfully",
        "id": book_id,
        "title": title,
        "author": author
    }), 200


# ==========================================
# DELETE BOOK
# ==========================================
@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    # Check if book exists
    cursor.execute(
        "SELECT id FROM books WHERE id = %s",
        (book_id,)
    )

    book = cursor.fetchone()

    if book is None:
        cursor.close()
        connection.close()

        return jsonify({
            "error": "Book not found"
        }), 404

    # Delete book
    cursor.execute(
        "DELETE FROM books WHERE id = %s",
        (book_id,)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Book deleted successfully",
        "id": book_id
    }), 200


# ==========================================
# RUN SERVER
# ==========================================
if __name__ == "__main__":
    app.run(debug=True)