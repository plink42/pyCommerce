import random
import string
import json

from flask import render_template, session, request, url_for, redirect
from sqlalchemy.dialects.mysql import DECIMAL
from sqlalchemy.dialects import sqlite

from app import app
from app import db

STORE_NAME = 'Movie Time Place'

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

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer(), primary_key=True)
    sessid = db.Column(db.Integer())
    item = db.Column(db.String(20), nullable=False)
    qty = db.Column(db.Integer(), default=1)
    cost = db.Column(DECIMAL(10,2), nullable=False)

    def __repr__(self):
        return '<Cart %r>'%self.sessid

@app.context_processor
def get_cart_count():
    """return total items in cart
    
    Returns:
        int -- count of all items in cart
    """

    cartitems = 0
    for i in Cart.query.filter(Cart.sessid == session['cartid']).all():
        cartitems += i.qty
    return dict(cartitems = cartitems)

@app.context_processor
def store_name():
    return dict(store_name=STORE_NAME)

@app.route('/')
def index():
    if 'cartid' not in session:
        randomsess = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
        session['cartid'] = randomsess
    prods = Products.query.order_by('street desc').limit(50).all()
    return render_template('index.html', prods = prods)

@app.route('/store')
def store():
    if 'cartid' not in session:
        randomsess = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
        session['cartid'] = randomsess
    prods = Products.query.order_by('street desc').limit(50).all()
    c = []
    for i in Cart.query.filter(Cart.sessid == session['cartid']).with_entities(Cart.item).all():
        c.append(i.item)    
    return render_template('store.html', prods = prods, incart= c)

@app.route('/add_to_cart/<upc>/<cost>')
def add_to_cart(upc, cost):
    if 'cartid' not in session:
        randomsess = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
        session['cartid'] = randomsess
    if upc:
        incart = Cart.query.filter(Cart.item == upc).filter(Cart.sessid == session['cartid']).all()
        if incart:
            Cart.query.filter(Cart.item == upc).filter(Cart.sessid == session['cartid']).update({Cart.qty: Cart.qty +1})
            db.session.commit()
        else:
            itemadd = Cart(sessid=session['cartid'], item=upc, qty=1, cost=cost)
            db.session.add(itemadd)
            db.session.commit()
    return redirect(url_for('show_cart'))

@app.route('/delete_from_cart/<upc>')
def delete_from_cart(upc):
    if upc:
        incart = Cart.query.filter(Cart.item == upc).filter(Cart.sessid == session['cartid']).all()
        if incart:
            Cart.query.filter(Cart.item == upc).filter(Cart.sessid == session['cartid']).delete()
            db.session.commit()
    return redirect(url_for('show_cart'))

@app.route('/update_cart/<upc>')
def update_cart(upc):
    qty = request.args.get('qty')
    if qty:
        if upc:
            incart = Cart.query.filter(Cart.item == upc).filter(Cart.sessid == session['cartid']).all()
            if incart:
                Cart.query.filter(Cart.item == upc).filter(Cart.sessid == session['cartid']).update({Cart.qty: qty})
                db.session.commit()
    return redirect(url_for('show_cart'))
    
@app.route('/cart')
def show_cart():
    thecart = Cart.query.filter(Cart.sessid == session['cartid']).all()
    cartdisp = []

    cart_total = 0
    for cart in thecart:
        prod = Products.query.filter(Products.upc == cart.item).limit(1).all()
        total = cart.cost*cart.qty
        data = {'upc': cart.item, 'cost': cart.cost, 'qty': cart.qty, 'title': prod[0].title, 'cust': prod[0].cust, 'total': total}
        cart_total += total
        cartdisp.append(data)
    return render_template('cart.html', thecart = cartdisp, cart_total = cart_total)

@app.route('/checkout')
def checkout_1():
    return render_template('checkout_1.html')

@app.route('/checkout/info')
def checkout_2():
    thecart = Cart.query.filter(Cart.sessid == session['cartid']).all()
    cart_total = 0
    for cart in thecart:
        total = cart.cost*cart.qty
        cart_total += total
    return render_template('checkout_2.html', cart_total=cart_total)

@app.route('/checkout/payment')
def checkout_3():
    return ''

@app.route('/getstates/<country>')
def get_states(country):
    with open('app/static/json/provinces.json', encoding='utf-8') as f:
        data = json.load(f)
    output = {}
    for i in data:
        if i['country'].upper() == country.upper():
            try:
                short = i['short']
            except:
                short = False
            if not short:
                output[i['name']] = i['name']
            else:
                output[short] = i['name']
    return json.dumps(output, indent=4)