#!/usr/bin/env python3

import sqlite3

db = sqlite3.connect("expense.db")

db.execute("""CREATE TABLE users (
           id INTEGER PRIMARY KEY,
           username TEXT NOT NULL,
           password_hash TEXT NOT NULL);""")

db.execute("""CREATE TABLE category (
           id INTEGER PRIMARY KEY, 
           category_name TEXT NOT NULL);""")

db.execute("""CREATE TABLE expense (
           id INTEGER PRIMARY KEY,
           user_id INTEGER NOT NULL,
           category_id INTEGER NOT NULL, 
           amount REAL NOT NULL, 
           date DATE NOT NULL,
           description TEXT, 
           FOREIGN KEY (user_id) REFERENCES users(id));""")

db.execute("""CREATE TABLE budget (
           id INTEGER PRIMARY KEY,
           category_id INTEGER NOT NULL,
           user_id INTEGER NOT NULL,
           amount REAL NOT NULL,
           start DATE NOT NULL,
           end DATE NOT NULL,
           FOREIGN KEY (category_id) REFERENCES category(id), 
           FOREIGN KEY (user_id) REFERENCES users(id));""")

db.execute("""INSERT INTO category (category_name)
           VALUES ("Food & Groceries"), ("Housing"),
           ("Transportation"), ("Healthcare"), ("Entertainment"),
           ("Education"), ("Debt Payments"), ("Savings & Investments"),
           ("Travel"), ("Utilities"), ("Clothing & Accessories"), ("Miscellaneous");""")

db.close()


