import random
import string
import json

from flask import render_template, session, request, url_for, redirect
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

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer(), primary_key=True)
    sessid = db.Column(db.Integer())
    item = db.Column(db.String(20), nullable=False)
    qty = db.Column(db.Integer(), default=1)
    cost = db.Column(DECIMAL(10,2), nullable=False)

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
def store_info():
    return dict(store_name=app.config['STORE_NAME'], 
        store_title=app.config['STORE_TITLE'],
        company_name=app.config['COMPANY_NAME'],
        site_url=app.config['STORE_URL'],
        twitter_url=app.config['TWITTER'],
        facebook_url=app.config['FACEBOOK'],
        instagram_url=app.config['INSTAGRAM'],
        home_url=app.config['HOME_PAGE'],
        domestic = app.config['DOMESTIC_COUNTRY'])

@app.route('/')
def index():
    if 'cartid' not in session:
        randomsess = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
        session['cartid'] = randomsess
    prods = Products.query.order_by('street desc').limit(50).all()
    return render_template('index.html', prods = prods)

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/about')
def about():
    return render_template('about.html')

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
    if 'cartid' not in session:
        randomsess = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
        session['cartid'] = randomsess
    thecart = Cart.query.filter(Cart.sessid == session['cartid']).all()
    cartdisp = []

    cart_total = 0
    for cart in thecart:
        prod = Products.query.filter(Products.upc == cart.item).limit(1).all()
        total = cart.cost*cart.qty
        data = {'upc': cart.item, 'cost': cart.cost, 'qty': cart.qty, 'title': prod[0].title, 'cust': prod[0].cust, 'total': '{:0.2f}'.format(total)}
        cart_total += total
        cartdisp.append(data)
    return render_template('cart.html', thecart = cartdisp, cart_total = '{:0.2f}'.format(cart_total))

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
    return render_template('checkout_2.html', cart_total='{:0.2f}'.format(cart_total))

@app.route('/checkout/shipping', methods=["GET", "POST"])
def checkout_3():
    if request.method == "GET":
        return redirect(url_for('show_cart'))
    if request.form['shipcountry'] == app.config['DOMESTIC_COUNTRY']:
        filt = 'domestic'
    else:
        filt = 'international'
    shipping = Shipping.query.filter(Shipping.region == filt).all()
    cartitems = get_cart_count()['cartitems']
    ship_options = []
    for s in shipping:
        if cartitems < s.maxqty:
            opt = {'id': s.id, 'name': s.name, 'description': s.description, 'total_cost': '{:0.2f}'.format(s.costper), 'isdefault': s.isdefault}
            ship_options.append(opt)
        else:
            cost = float(s.costper + (cartitems - s.maxqty) * s.additional)
            cost = '{:0.2f}'.format(cost)
            opt = {'id': s.id, 'name': s.name, 'description': s.description, 'total_cost': cost, 'isdefault': s.isdefault}
            ship_options.append(opt)
    print(ship_options)

    if request.method == "POST":
        return render_template('checkout_3.html', person=request.form, ship_options=ship_options)
    

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