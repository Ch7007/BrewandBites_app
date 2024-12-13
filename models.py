from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import sessionmaker, declarative_base

# Base for all models
Base = declarative_base()

# User Model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)  # Will be stored encrypted
    email = Column(String, nullable=False, unique=True)
    role = Column(String, nullable=False)  # 'admin' or 'user'

# Expense Model
class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)

# Inventory Model
class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True, autoincrement=True)
    item_name = Column(String, nullable=False, unique=True)
    quantity = Column(Integer, nullable=False)
    cost = Column(Float, nullable=False)

# Sales Model
class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    items_sold = Column(String, nullable=False)  # Comma-separated list of items

# Initialize the database
def init_db(db_path):
    """
    Creates the SQLite database and all tables if they don't exist.
    """
    engine = create_engine(db_path, echo=False)  # Set echo to True for debugging
    Base.metadata.create_all(engine)
    print("Database initialized successfully!")
    return engine

# For creating sessions (to be used in DAL)
def get_session(engine):
    """
    Returns a new session for the database.
    """
    Session = sessionmaker(bind=engine)
    return Session()
