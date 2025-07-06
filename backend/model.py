# Importing libraries
import sqlite3 
from config import Config 

# creating a function to connect to batabase
def connect_db():
    con = sqlite3.connect(Config.DATABASE)
    con.row_factory = sqlite3.Row 
    return con

# Creating a function for creating table in database
def init_db():
    with connect_db() as con:
        cur = con.cursor()
        cur.excute("""
        CREATE TABLE users(
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           username TEXT UNIQUE,
           password TEXT,
           role TEXT CHECK(role IN('admin', 'cashier))
        )""")
        cur.excute("""
        CREATE TABLE products (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           name TEXT,
           price REAL,
           quantity INTEGER
        )""")
        cur.excute("""
        CREATE TABLE sales(
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           product_id INTEGER,
           quantity INTEGER,
           total_price REAL,
           payment_type TEXT,
           trans_date TEXT,
         )""")
         cur.execute("""
        CREATE TABLE expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            amount REAL,
            exp_date TEXT
        )""")
        con.commit()

     

