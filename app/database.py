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
    `name` BLOB,
    `longdescription` TEXT,
    `shortdescription` TEXT,
    `price` NUMERIC,
    `retailPrice` NUMERIC,
    `weight` NUMERIC,
    `thumb` BLOB,
    `image` BLOB,
    `updateDate` NUMERIC,
    `categories` BLOB,
    `liveDate` NUMERIC, 
    `stock` INTEGER,
    `isFeatured` INTEGER DEFAULT 0)'''

conn.execute(Products)

ProductOptions = '''CREATE TABLE "productoptions"
    (`id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `optionid` INTEGER,
    `productid` INTEGER,
    `optiongroupid` INTEGER,
    `optionpriceincrement` NUMERIC)'''

conn.execute(ProductOptions)

Options = '''CREATE TABLE "options"
    (`id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `optionname` BLOB)'''

conn.execute(Options)

OptionGroups = '''CREATE TABLE "optiongroups"
    (`id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `groupname` BLOB)'''

conn.execute(OptionGroups)

Categories = '''CREATE TABLE "categories"
    (`id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `name` BLOB,
    `description` BLOB,
    `image` BLOB)'''

conn.execute(Categories)

Orders = '''CREATE TABLE "orders"
    (`id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `userid` INTEGER,
    `orderamout` NUMERIC,
    `shipname` BLOB,
    `shipaddress1` BLOB,
    `shipaddress2` BLOB,
    `shipcity` BLOB,
    `shipstate` BLOB,
    `shipzip` BLOB,
    `shipcountry` BLOB,
    `shipphone` BLOB,
    `shipid` INTEGER,
    `tax` NUMERIC,
    `email` BLOB,
    `shipcost` NUMERIC,
    `orderdate` NUMERIC,
    `statusid` INTEGER,
    `statusdate`, NUMERIC,
    `trackingnumber`, BLOB)'''

conn.execute(Orders)

Statuses = '''CREATE TABLE "statuses"
    (`id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `description` BLOB,
    `emailtemplateid` INTEGER)'''

conn.execute(Statuses)

OrderDetails = '''CREATE TABLE "orderdetails"
    (`id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `orderid` INTEGER,
    `productid` INTEGER,
    `price` NUMERIC,
    `qty` INTEGER)'''

conn.execute(OrderDetails)

Users = '''CREATE TABLE "users"
    (`id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `email` BLOB,
    `passwd` BLOB,
    `firstname` BLOB,
    `lastname` BLOB,
    `billaddress1` BLOB,
    `billaddress2` BLOB,
    `billcity` BLOB,
    `billstate` BLOB
    `billzip` BLOB,
    `billcountry` BLOB,
    `registrationdate` NUMERIC,
    `ip` BLOB)'''

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