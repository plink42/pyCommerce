import sqlite3
import sys

try:
    dbname = sys.argv[1]
except:
    print('usage: python database.py [dbname.db]')
    exit()
#Open database
conn = sqlite3.connect(dbname)

Products = '''CREATE TABLE "products"
    (`id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `sku` BLOB,
    `title` BLOB,
    `synopsis` TEXT,
    `suggestedRetail` NUMERIC,
    `cust` BLOB,
    `street` NUMERIC,
    `isFeatured` INTEGER DEFAULT 0)'''

conn.execute(Products)

Cart = '''CREATE TABLE "cart" 
    ( `id` INTEGER PRIMARY KEY AUTOINCREMENT, 
    `sessid` BLOB, 
    `item` BLOB, 
    `qty` INTEGER, 
    `cost` NUMERIC, 
    `date` NUMERIC )'''

conn.execute(Cart)

Shipping = '''CREATE TABLE "shipping" ( `id` INTEGER PRIMARY KEY AUTOINCREMENT, 
    `name` BLOB, 
    `description` BLOB, 
    `costper` NUMERIC, 
    `maxqty` INTEGER, 
    `additional` NUMERIC, 
    `region` BLOB, 
    `isdefault` INTEGER DEFAULT 0 )'''

conn.execute(Shipping)