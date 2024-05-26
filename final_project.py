from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from modules import Base, Category, Book, Order, OrderBook
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

engine = create_engine('sqlite:///library.db', echo=True)
Session = sessionmaker(bind=engine)
db_session = Session()

db = SQLAlchemy(app)
db.Model.metadata.create_all(engine)

#@app.route('/')
#def index():
  #  return "library"


@app.route('/categories', methods=['POST'])
def add_category():
    data = request.json
    new_category = Category( id =data['id'] ,Cname=data['Cname'])
    db_session.add(new_category)
    try:
        db_session.commit()
        return jsonify({'message': 'Category added successfully'}), 201
    except IntegrityError:
        db_session.rollback()
        return jsonify({'error': 'Category already exists'}), 400


categoryOne = Category(id = 1 , Cname='Fiction')
db_session.add(categoryOne)
categoryTwo = Category(id = 2 , Cname='Non-Fiction')
db_session.add(categoryTwo)
db_session.commit() 

@app.route('/categories', methods=['GET'])
def get_categories():
    categories = db_session.query(Category).all()
    return jsonify([category.__dict__ for category in categories]), 200


# Routes for Books
# adding a new book
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    category_id = data.get('category_id')  # Assuming category_id is provided in the request data
    category = Category.query.get(category_id)
    if not category:
        return jsonify({'message': 'Category not found!'}), 404
    
    new_book = Book(title=data['title'], author=data['author'], price=data['price'], quantity=data['quantity'], category=category)
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully'}), 201

# Create a new book
bookOne = Book(title='python ', author='tamara', price=29.99, quantity=10, category=categoryOne)
db_session.add(bookOne)
bookTwo = Book(title='C++', author='Ahmad', price=29.99, quantity=10, category=categoryOne)
db_session.add(bookTwo)
bookThree = Book(title='Html , css', author='Ali', price=29.99, quantity=10, category=categoryOne)
db_session.add(bookThree)
db_session.commit()


# API route for retrieving all books
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    if not books:
        return jsonify({'message': 'No books found'}), 404
    
    books_data = []
    for book in books:
        books_data.append({'id': book.id, 'title': book.title, 'author': book.author, 'price': book.price, 'quantity': book.quantity, 'category': book.category.Cname})
    
    return jsonify({'books': books_data}), 200

# API route for retrieving a specific book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    
    book_data = {'id': book.id, 'title': book.title, 'author': book.author, 'price': book.price, 'quantity': book.quantity, 'category': book.category.Cname}
    return jsonify({'book': book_data}), 200

# API route for updating a specific book by ID
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.price = data.get('price', book.price)
    book.quantity = data.get('quantity', book.quantity)
    db.session.commit()
    return jsonify({'message': 'Book updated successfully'}), 200

# API route for deleting a specific book by ID
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'}), 200

# Routes for Orders
@app.route('/orders', methods=['GET'])
def get_orders():
    orders = db_session.query(Order).all()
    return jsonify([order.__dict__ for order in orders]), 200

@app.route('/orders', methods=['POST'])
def add_order():
    data = request.json
    new_order = Order(date_of_purchase=datetime.utcnow())
    db_session.add(new_order)
    try:
        db_session.commit()
        return jsonify({'message': 'Order added successfully'}), 201
    except IntegrityError:
        db_session.rollback()
        return jsonify({'error': 'Failed to add order'}), 400

# API route for retrieving a specific order by ID
@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404
    
    order_books = [{'title': book.title, 'author': book.author, 'quantity': order_book.quantity} for book, order_book in order.books]
    order_data = {'id': order.id, 'date_of_purchase': order.date_of_purchase, 'books': order_books}
    
    return jsonify({'order': order_data}), 200

# API route for retrieving all orders
@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    if not orders:
        return jsonify({'message': 'No orders found'}), 404
    
    orders_data = []
    for order in orders:
        order_books = [{'title': book.title, 'author': book.author, 'quantity': order_book.quantity} for book, order_book in order.books]
        order_data = {'id': order.id, 'date_of_purchase': order.date_of_purchase, 'books': order_books}
        orders_data.append(order_data)
    
    return jsonify({'orders': orders_data}), 200

# deleting a specific order by ID 
@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = db_session.query(Order).filter_by(id=order_id).first()
    if order:
        db_session.delete(order)
        db_session.commit()
        return jsonify({'message': 'Order deleted successfully'}), 200
    else:
        return jsonify({'error': 'Order not found'}), 404



if __name__ == '__main__':
    app.run(debug=True)
