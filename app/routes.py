from flask import render_template, session, request, flash, url_for, redirect, g
from sqlalchemy.dialects.mysql import DECIMAL
from sqlalchemy.dialects import sqlite

from app import app
from app import db

class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer(), primary_key=True)
    upc = db.Column(db.String(14), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    synopsis = db.Column(db.Text, nullable=False)
    suggestedRetail = db.Column(DECIMAL(10, 2), nullable=False)
    cust = db.Column(db.String(200), nullable=False)
    street = db.Column(sqlite.DATE(storage_format="%(year)04d-%(month)02d-%(day)02d"))

    def __repr__(self):
        return '<Product %r>'%self.upc


@app.route('/')
def index():
    prods = Products.query.order_by('street desc').limit(50).all()
    return render_template('index.html', prods = prods)
