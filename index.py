from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from datetime import datetime
from bson.objectid import ObjectId  # For working with MongoDB ObjectIds

app = Flask(__name__)
app.secret_key = 'admin420'  # Replace with a strong secret key

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb+srv://89aman:123456789poiuytrewq@myatlasclusteredu.pgfc8.mongodb.net/library_management?retryWrites=true&w=majority"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

# Accessing collections
books_collection = mongo.db.books
records_collection = mongo.db.records

# Helper function to check if user is logged in
def is_logged_in():
    return 'username' in session

# Home route
@app.route('/')
def home():
    return render_template('base.html')

# Add Book Route (Protected)
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if not is_logged_in():
        flash('You must be logged in to add books.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        publisher = request.form['publisher']
        isbn = request.form['isbn']
        year = request.form['year']

        new_book = {
            'title': title,
            'author': author,
            'genre': genre,
            'isbn': isbn,
            'year': year,
            'publisher': publisher,
            'available': True  # Newly added books are available by default
        }

        # Insert the book into the books collection
        books_collection.insert_one(new_book)

        flash('Book added successfully!', 'success')
        return render_template('dashboard.html')

    return render_template('add_book.html')

# Borrow Book Route (Protected)
@app.route('/borrow/<book_id>', methods=['POST'])
def borrow_book(book_id):
    if not is_logged_in():
        flash('You must be logged in to borrow books.', 'warning')
        return redirect(url_for('login'))

    # Check if the book is available
    book = books_collection.find_one({'_id': ObjectId(book_id)})

    if book and book['available']:
        # Borrow the book
        username = session.get('username')  # Get the logged-in user's username
        borrowed_date = datetime.now().strftime('%Y-%m-%d')

        # Add a new record for the borrowed book
        new_record = {
            'book_id': book['_id'],
            'user_id': username,
            'borrowed_date': borrowed_date,
            'returned_date': None  # Not returned yet
        }

        # Insert the record into the records collection
        records_collection.insert_one(new_record)

        # Update the book's availability status
        books_collection.update_one({'_id': book['_id']}, {'$set': {'available': False}})

        flash('Book borrowed successfully!', 'success')
        return redirect(url_for('dashboard'))

    flash('Book is not available.', 'danger')
    return redirect(url_for('dashboard'))

# Return Book Route (Protected)
@app.route('/return/<book_id>', methods=['POST'])
def return_book(book_id):
    if not is_logged_in():
        flash('You must be logged in to return books.', 'warning')
        return redirect(url_for('login'))

    # Find the record of the borrowed book
    record = records_collection.find_one({'book_id': ObjectId(book_id), 'returned_date': None})

    if record:
        # Update the record with the return date
        returned_date = datetime.now().strftime('%Y-%m-%d')
        records_collection.update_one(
            {'_id': record['_id']},
            {'$set': {'returned_date': returned_date}}
        )

        # Update the book's availability
        books_collection.update_one(
            {'_id': ObjectId(book_id)},
            {'$set': {'available': True}}
        )

        flash('Book returned successfully!', 'success')
        return redirect(url_for('dashboard'))

    flash('No record found for borrowing this book.', 'danger')
    return redirect(url_for('dashboard'))

# Dashboard Route (Protected)
@app.route('/dashboard')
def dashboard():
    if not is_logged_in():
        flash('You need to login first', 'warning')
        return redirect(url_for('login'))

    username = session['username']

    # Get the list of books borrowed by the user
    borrowed_books = records_collection.find({'user_id': username, 'returned_date': None})
    books = []
    for record in borrowed_books:
        book = books_collection.find_one({'_id': record['book_id']})
        if book:
            books.append(book)

    return render_template('dashboard.html', books=books)

# Login Route (as before)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Fetch user from the database
        user = mongo.db.users.find_one({'username': username})

        if user and bcrypt.check_password_hash(user['password'], password):
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

# Logout Route
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register'))

        # Check if the username already exists
        existing_user = mongo.db.users.find_one({'username': username})
        if existing_user:
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))

            # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            # Create a new user document
        new_user = {
            'username': username,
            'password': hashed_password
            }

            # Insert the new user into the users collection
        mongo.db.users.insert_one(new_user)

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')
    

if __name__ == "__main__":
    app.run()