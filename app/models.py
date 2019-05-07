from app import db

from sqlalchemy.dialects.mysql import DECIMAL
from sqlalchemy.dialects import sqlite

class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer(), primary_key=True)
    sku = db.Column(db.String(14), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    synopsis = db.Column(db.Text, nullable=False)
    suggestedRetail = db.Column(DECIMAL(10, 2), nullable=False)
    cust = db.Column(db.String(200), nullable=False)
    street = db.Column(sqlite.DATE(storage_format="%(year)04d-%(month)02d-%(day)02d"))
    isFeatured = db.Column(db.Integer())

    def __repr__(self):
        return '<Product %r>'%self.sku

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer(), primary_key=True)
    sessid = db.Column(db.Integer())
    item = db.Column(db.String(20), nullable=False)
    qty = db.Column(db.Integer(), default=1)
    cost = db.Column(DECIMAL(10,2), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)

    def __repr__(self):
        return '<Cart %r>'%self.sessid

class Shipping(db.Model):
    __tablename__ = 'shipping'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    costper = db.Column(DECIMAL(10,2), nullable=False)
    maxqty = db.Column(db.Integer())
    additional = db.Column(DECIMAL(10,2))
    isdefault = db.Column(db.Integer(), default=0)
    region = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Shipping %r>'%self.name