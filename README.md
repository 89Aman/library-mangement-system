# Library Management System

This project is a simple Library Management System built with Flask and MongoDB. It allows users to manage books, user records, and transactions related to book borrowing in an easy-to-use web interface.

## Features

- **Manage Books**: Add, update, and delete books in the library.
- **User Management**: Track users with their personal information and borrowed books.
- **Borrowing Records**: Keep track of books borrowed by users and their due dates.
- **MongoDB Integration**: Utilizes MongoDB to store all data in collections (`books`, `users`, `records`).

## Tech Stack

- **Backend**: Flask
- **Database**: MongoDB (MongoDB Atlas Cloud Database)
- **Authentication**: No authentication system included yet (can be extended)
- **Python Libraries**:
  - `Flask`
  - `Flask-PyMongo`

## Setup and Installation

Follow the steps below to set up the project on your local machine.

### Prerequisites

1. Python 3.7 or higher.
2. A MongoDB Atlas account with a database set up.
3. Install dependencies with pip.

### Clone the repository

```bash
git clone https://github.com/your-username/library-management-system.git
cd library-management-system
```

### Install dependencies

Create a virtual environment (optional but recommended) and install the necessary dependencies:

```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows

pip install -r requirements.txt
```

### Configure MongoDB URI

1. Go to your MongoDB Atlas account and obtain your connection string.
2. Replace `<db_username>`, `<db_password>`, and `<cluster_address>` in the connection string in `app.py`:

```python
app.config["MONGO_URI"] = "mongodb+srv://<db_username>:<db_password>@<cluster_address>/<database_name>?retryWrites=true&w=majority"
```

Make sure to set the correct database name (`library_management`) and the collection names (`books`, `users`, `records`).

### Run the Application

Start the Flask development server:

```bash
flask run
```

By default, the application will be available at `http://127.0.0.1:5000`.

## API Endpoints

### /books
- **GET**: Retrieve a list of all books.
- **POST**: Add a new book to the library.
- **PUT**: Update a book's details.
- **DELETE**: Delete a book from the library.

### /users
- **GET**: Retrieve a list of all users.
- **POST**: Add a new user to the library system.
- **PUT**: Update a user's information.
- **DELETE**: Delete a user from the system.

### /records
- **GET**: Retrieve all borrowing records.
- **POST**: Add a new borrowing record (book borrowed by user).
- **PUT**: Update a borrowing record.
- **DELETE**: Delete a borrowing record.

## File Structure

```
/library-management-system
├── app.py                # Main Flask application
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
└── /templates            # HTML templates (if any)
└── /static               # Static files (CSS, JS, Images, etc.)
```

## Contributing

Contributions are welcome! Feel free to open an issue or create a pull request.

## License

This project is open-source and available under the [MIT License](LICENSE).

---