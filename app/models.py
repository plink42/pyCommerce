from app import db

from sqlalchemy.dialects.mysql import DECIMAL
from sqlalchemy.dialects import sqlite

class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer(), primary_key=True)
    sku = db.Column(db.String(14), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    longdescription = db.Column(db.Text, nullable=False)
    shortdescription = db.Column(db.Text, nullable=False)
    price = db.Column(db.String(14), nullable=False)
    retailPrice = db.Column(db.String(14), nullable=False)
    weight = db.Column(db.String(14), nullable=False)
    thumb = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    image_other = db.Column(db.String(255), nullable=False)
    updateDate = db.Column(sqlite.DATE(storage_format="%(year)04d-%(month)02d-%(day)02d"))
    categories = db.Column(db.String(255), nullable=False)
    liveDate = db.Column(sqlite.DATE(storage_format="%(year)04d-%(month)02d-%(day)02d"))
    stock = db.Column(db.Integer())
    isFeatured = db.Column(db.Integer())

    def __repr__(self):
        return '<Product %r>'%self.sku

class ProductOptions(db.Model):
    __tablename__ = 'productoptions'
    id = db.Column(db.Integer(), primary_key=True)
    optionid = db.Column(db.Integer(), db.ForeignKey('options.id'))
    productid = db.Column(db.Integer(), db.ForeignKey('products.id'))
    optiongroupid = db.Column(db.Integer(), db.ForeignKey('optiongroups.id'))
    optionpriceincrement = db.Column(db.String(14))

    def __repr__(self):
        return '<ProductOptions %r>'%self.id

class Options(db.Model):
    __tablename__ = 'options'
    id = db.Column(db.Integer(), primary_key=True)
    optionname = db.Column(db.String(255))

    def __repr__(self):
        return '<Options %r>'%self.id
    
class OptionGroups(db.Model):
    __tablename__ = 'optiongroups'
    id = db.Column(db.Integer(), primary_key=True)
    groupname = db.Column(db.String(255))

    def __repr__(self):
        return '<OptionGroups %r>'%self.id

class Categories(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    image = db.Column(db.String(255))

    def __repr__(self):
        return '<Cateogries %r>'%self.name

class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer(), primary_key=True)
    userid = db.Column(db.Integer(), db.ForeignKey('users.id'))
    orderamount = db.Column(db.String(14))
    shipname = db.Column(db.String(255))
    shipaddress1 = db.Column(db.String(255))
    shipaddress2 = db.Column(db.String(255))
    shipcity = db.Column(db.String(255))
    shipstate = db.Column(db.String(255))
    shipzip = db.Column(db.String(10))
    shipcountry = db.Column(db.String(255))
    shipphone = db.Column(db.String(255))
    shipid = db.Column(db.Integer(), db.ForeignKey('shipping.id'))
    tax = db.Column(db.String(14))
    email = db.Column(db.String(255))
    shipcost = db.Column(db.String(14))
    orderdate = db.Column(sqlite.DATE(storage_format="%(year)04d-%(month)02d-%(day)02d"))
    statusid = db.Column(db.Integer(), db.ForeignKey('statuses.id'))
    statusdate = db.Column(sqlite.DATE(storage_format="%(year)04d-%(month)02d-%(day)02d"))
    trackingnumber = db.Column(db.String(255))

    def __repr__(self):
        return '<Orders %r>'%self.id

class Statuses(db.Model):
    __tablename__ = 'statuses'
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(50))
    emailtemplateid = db.Column(db.Integer())

    def __repr__(self):
        return '<Statuses %r>'%self.description

class OrderDetails(db.Model):
    __tablename__ = 'orderdetails'
    id = db.Column(db.Integer(), primary_key=True)
    orderid = db.Column(db.Integer(), db.ForeignKey('orders.id'))
    productid = db.Column(db.Integer(), db.ForeignKey('products.id'))
    price = db.Column(db.String(14))
    qty = db.Column(db.Integer())

    def __repr__(self):
        return '<OrderDetails %r>'%self.id

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255))
    passwd = db.Column(db.String(255))
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    billaddress1 = db.Column(db.String(255))
    billaddress2 = db.Column(db.String(255))
    billcity = db.Column(db.String(255))
    billstate = db.Column(db.String(255))
    billzip = db.Column(db.String(255))
    billcountry = db.Column(db.String(255))
    registrationdate = db.Column(sqlite.DATE(storage_format="%(year)04d-%(month)02d-%(day)02d"))
    ip = db.Column(db.String(255))

    def __repr__(self):
        return '<Users %r>'%self.id

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer(), primary_key=True)
    sessid = db.Column(db.Integer())
    item = db.Column(db.String(20), nullable=False)
    qty = db.Column(db.Integer(), default=1)
    cost = db.Column(db.String(14), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)

    def __repr__(self):
        return '<Cart %r>'%self.sessid

class Shipping(db.Model):
    __tablename__ = 'shipping'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    costper = db.Column(db.String(14), nullable=False)
    maxqty = db.Column(db.Integer())
    additional = db.Column(db.String(14))
    isdefault = db.Column(db.Integer(), default=0)
    region = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Shipping %r>'%self.name