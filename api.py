from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/books'  # MongoDB connection URI
mongo = PyMongo(app)

# GET request to retrieve all books
@app.route('/books', methods=['GET'])
def get_books():
    books = mongo.db.books.find()
    book_list = []
    for book in books:
        book['_id'] = str(book['_id'])  # Convert ObjectId to string
        book_list.append(book)
    return jsonify(book_list)

# GET request to retrieve a specific book by ID
@app.route('/books/<string:book_id>', methods=['GET'])
def get_book(book_id):
    book = mongo.db.books.find_one({'_id': book_id})
    if book:
        book['_id'] = str(book['_id'])  # Convert ObjectId to string
        return jsonify(book)
    return jsonify({'error': 'Book not found'}), 404

# POST request to add a new book
@app.route('/books', methods=['POST'])
def add_book():
    book_data = request.get_json()
    book_id = mongo.db.books.insert_one(book_data).inserted_id
    book = mongo.db.books.find_one({'_id': book_id})
    book['_id'] = str(book['_id'])  # Convert ObjectId to string
    return jsonify(book), 201

# PUT request to update an existing book
@app.route('/books/<string:book_id>', methods=['PUT'])
def update_book(book_id):
    book_data = request.get_json()
    result = mongo.db.books.update_one({'_id': book_id}, {'$set': book_data})
    if result.modified_count == 1:
        book = mongo.db.books.find_one({'_id': book_id})
        book['_id'] = str(book['_id'])  # Convert ObjectId to string
        return jsonify(book)
    return jsonify({'error': 'Book not found'}), 404

# DELETE request to remove a book
@app.route('/books/<string:book_id>', methods=['DELETE'])
def delete_book(book_id):
    result = mongo.db.books.delete_one({'_id': book_id})
    if result.deleted_count == 1:
        return jsonify({'result': 'Book deleted'})
    return jsonify({'error': 'Book not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
