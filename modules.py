from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

engine = create_engine('sqlite:///library.db', echo=True)
Base = declarative_base()

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    Cname = Column(String, unique=True, nullable=False)

    # Relationship (one-to-many: Category->Books)
    books = relationship("Book", back_populates="category")

class OrderBook(Base):
    __tablename__ = 'order_books'
    order_id = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)

    # the relationship to the Order table
    order = relationship("Order", back_populates="order_books")

    # the relationship to the Book table
    book = relationship("Book", back_populates="order_books")

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))

    # Relationship (many-to-one: Book->Category)
    category = relationship("Category", back_populates="books")
    # many-to-many relationship (Order <-> Book)
    order_books = relationship("OrderBook", back_populates="book")

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    date_of_purchase = Column(DateTime, default=datetime.utcnow)
    
    order_books = relationship("OrderBook", back_populates="order")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

