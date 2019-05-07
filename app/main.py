import random
import string
import json
import datetime

from flask import render_template, session, request, url_for, redirect
from sqlalchemy.sql import func

from app import app
from app import db
from app import models


db.init_app(app)

@app.context_processor
def get_cart_count():
    """return total items in cart
    
    Returns:
        int -- count of all items in cart
    """

    cartitems = 0
    for i in models.Cart.query.filter(models.Cart.sessid == session['cartid']).all():
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
    featured = models.Products.query.filter(models.Products.isFeatured == 1).all()
    randos = models.Products.query.order_by(func.random()).limit(10).all()
    return render_template('index.html', featured = featured, randos=randos)

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
    prods = models.Products.query.order_by('street desc').limit(50).all()
    c = []
    for i in models.Cart.query.filter(models.Cart.sessid == session['cartid']).with_entities(models.Cart.item).all():
        c.append(i.item)    
    return render_template('store.html', prods = prods, incart= c)

@app.route('/add_to_cart/<sku>/<cost>')
def add_to_cart(sku, cost):
    if 'cartid' not in session:
        randomsess = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
        session['cartid'] = randomsess
    if sku:
        incart = models.Cart.query.filter(models.Cart.item == sku).filter(models.Cart.sessid == session['cartid']).all()
        if incart:
            models.Cart.query.filter(models.Cart.item == sku).filter(models.Cart.sessid == session['cartid']).update({models.Cart.qty: models.Cart.qty +1})
            db.session.commit()
        else:
            itemadd = models.Cart(sessid=session['cartid'], item=sku, qty=1, cost=cost, date=datetime.datetime.now())
            db.session.add(itemadd)
            db.session.commit()
    return redirect(url_for('show_cart'))

@app.route('/delete_from_cart/<sku>')
def delete_from_cart(sku):
    if sku:
        incart = models.Cart.query.filter(models.Cart.item == sku).filter(models.Cart.sessid == session['cartid']).all()
        if incart:
            models.Cart.query.filter(models.Cart.item == sku).filter(models.Cart.sessid == session['cartid']).delete()
            db.session.commit()
    return redirect(url_for('show_cart'))

@app.route('/update_cart/<sku>')
def update_cart(sku):
    qty = request.args.get('qty')
    if qty:
        if sku:
            incart = models.Cart.query.filter(models.Cart.item == sku).filter(models.Cart.sessid == session['cartid']).all()
            if incart:
                models.Cart.query.filter(models.Cart.item == sku).filter(models.Cart.sessid == session['cartid']).update({models.Cart.qty: qty})
                db.session.commit()
    return redirect(url_for('show_cart'))
    
@app.route('/cart')
def show_cart():
    if 'cartid' not in session:
        randomsess = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
        session['cartid'] = randomsess
    thecart = models.Cart.query.filter(models.Cart.sessid == session['cartid']).all()
    cartdisp = []

    cart_total = 0
    for cart in thecart:
        prod = models.Products.query.filter(models.Products.sku == cart.item).limit(1).all()
        total = cart.cost*cart.qty
        data = {'sku': cart.item, 'cost': cart.cost, 'qty': cart.qty, 'title': prod[0].title, 'cust': prod[0].cust, 'total': '{:0.2f}'.format(total)}
        cart_total += total
        cartdisp.append(data)
    return render_template('cart.html', thecart = cartdisp, cart_total = '{:0.2f}'.format(cart_total))

@app.route('/checkout')
def checkout_1():
    return render_template('checkout_1.html')

@app.route('/checkout/info')
def checkout_2():
    thecart = models.Cart.query.filter(models.Cart.sessid == session['cartid']).all()
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
    shipping = models.Shipping.query.filter(models.Shipping.region == filt).all()
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