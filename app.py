from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from backendFiles.Authenticator import *
import json
from cart import *
from items_cart import cartItem
from payment import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stores.db'
app.secret_key = 'key'
# Initalise DB
db = SQLAlchemy(app)

# create db model
class Stores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    opening_hours = db.Column(db.String(50))
    petrols = db.relationship('Petrol', backref='store', lazy=True)

    def __repr__(self):
        return '<Name %r>' % self.id
    
class Petrol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)

    def __repr__(self):
        return '<Name %s, Price %s>' % (self.name, self.price)
    
class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.id
    
@app.route('/')
def index():
    return render_template('loginForCustomer.html')

@app.route('/addStore', methods=['GET','POST'])
def addStore():
    if request.method == "POST":
        name = request.form.get('name')
        address = request.form.get('address')
        opening_hours = request.form.get('opening_hours')
        if name and address:
            new_store = Stores(name=name, address=address, opening_hours=opening_hours)
            db.session.add(new_store)
            db.session.commit()
            return redirect(url_for('storesDisplay'))
    return render_template('addStore.html')

@app.route('/storesDisplay')
def storesDisplay():
    title = "Store List"
    stores = Stores.query.order_by(Stores.name.asc()).all()
    return render_template("storesDisplay.html", title=title, stores=stores)

@app.route('/storeDetails/<int:store_id>')
def storeDetails(store_id):
    store = Stores.query.get_or_404(store_id)
    return render_template('storeDetails.html', store=store)

@app.route('/addPetrol/<int:store_id>', methods=['GET', 'POST'])
def addPetrol(store_id):
    store = Stores.query.get_or_404(store_id)

    if len(store.petrols) >= 3:
        return redirect(url_for('storeDetails', store_id=store_id))
    
    if request.method == "POST":
        name = request.form.get('name')
        price = request.form.get('price')

        if name and price:
            new_petrol = Petrol(name=name, price=float(price), store_id=store_id)
            db.session.add(new_petrol)
            db.session.commit()
            return redirect(url_for('storeDetails', store_id=store_id))
        
    return render_template('addPetrol.html', store=store)

@app.route('/editPetrolPrice/<int:petrol_id>', methods=['GET', 'POST'])
def editPetrolPrice(petrol_id):
    petrol = Petrol.query.get_or_404(petrol_id)

    if request.method == "POST":
        new_price = request.form.get('price')
        if new_price:
            petrol.price = float(new_price)
            db.session.commit()
            return redirect(url_for('storeDetails', store_id=petrol.store_id))
        
    return render_template('editPetrolPrice.html', petrol=petrol)

@app.route('/customerStoresDisplay')
def customerStoresDisplay():
    title = "Store List"
    stores = Stores.query.order_by(Stores.name.asc()).all()
    return render_template("customerStoresDisplay.html", title=title, stores=stores)

@app.route('/customerStoreDetails/<int:store_id>', methods=['GET', 'POST'])
def customerStoreDetails(store_id):
    if request.method == 'POST':
        input_code = request.form['input_code']

    store = Stores.query.get_or_404(store_id)
    return render_template('customerStoreDetails.html', store=store)

@app.route('/storeDelete/<int:store_id>', methods=['GET', 'POST'])
def storeDelete(store_id):
    store = Stores.query.get_or_404(store_id)

    if request.method == "POST":
        Petrol.query.filter_by(store_id=store.id).delete()

        db.session.delete(store)
        db.session.commit()
        return redirect(url_for('storesDisplay'))
    
    return render_template('storeDelete.html', store=store)

@app.route('/editStore/<int:store_id>', methods=['GET', 'POST'])
def editStore(store_id):
    store = Stores.query.get_or_404(store_id)

    if request.method == "POST":
        new_name = request.form.get('name')
        new_opening_hours = request.form.get('opening_hours')
        new_address = request.form.get('address')
        if new_name or new_opening_hours or new_address:
            store.name = new_name
            store.opening_hours = new_opening_hours
            store.address = new_address
            db.session.commit()
            return redirect(url_for('storesDisplay'))

    return render_template('editStore.html', store=store)

@app.route('/loginForCustomer', methods=['GET','POST']) 
def loginForCustomer():

    if request.method == "POST":
        username = request.form.get('name')
        password = request.form.get('password')
        try:
            auth = Authenticator()
            auth.fillData()
            user = auth.login(username, password)
            print(user)
            if user!=None:
                #converts the user object to a json string which can be passed through
                userJson = json.dumps(user.__dict__) 
                print(userJson)
                session['user'] = userJson

                return redirect(url_for('customerIndex'))

        except InvalidUsername:
            return render_template('loginForCustomer.html', error="Invalid username")
        except InvalidPassword:
            return render_template('loginForCustomer.html', error="Invalid password")

    return render_template('loginForCustomer.html')

@app.route('/guestLogin')
def guestLogin():

   session['user'] = json.dumps(User("Guest","noPassword",0).__dict__) 
   print(session['user'])
   return redirect(url_for('customerIndex'))

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    if request.method == "POST":
        username = request.form.get('name')
        password = request.form.get('password')
        contactNumber= request.form.get('contactNum')

        try:
            auth = Authenticator()
            auth.addUser(username,password,contactNumber)

        except UsernameAlreadyExists:
            return render_template('signUp.html', error="Username Already Exists")
        except PasswordTooShort:
            return render_template('signUp.html', error="Password Too Short")

    return render_template('signUp.html')

@app.route('/customerIndex', methods=['GET', 'POST']) 
def customerIndex():
    #could be error from here
    if 'user' in session:
        #get the json user string and truns it back into a dict
        user_dict = json.loads(session['user'])
        return render_template('customerIndex.html', user=user_dict)  # Pass user to template

    return render_template('loginForCustomer.html', error="data could not be retrieved")

@app.route('/managerIndex', methods=['GET', 'POST'])
def managerIndex():
    if 'user' in session:
        user_dict = json.loads(session['user'])
        return render_template('managerIndex.html', user=user_dict)  # Pass user to template

    return render_template('loginForManager.html', error="data could not be retrieved")

@app.route('/loginForManager', methods=['GET','POST']) 
def loginForManager():

    if request.method == "POST":
        username = request.form.get('name')
        password = request.form.get('password')
        try:
            auth = Authenticator()
            auth.fillData()
            user = auth.login(username, password)
            print(user)
            if user!=None:
                #converts the user object to a json string which can be passed through
                userJson = json.dumps(user.__dict__) 
                print(userJson)
                session['user'] = userJson

                return redirect(url_for('managerIndex'))

        except InvalidUsername:
            return render_template('loginForManager.html', error="Invalid username")
        except InvalidPassword:
            return render_template('loginForManager.html', error="Invalid password")

    return render_template('loginForManager.html')

@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove user from session
    return redirect(url_for('loginForCustomer'))  # Redirect to the home page or login

@app.route('/menuList')
def menuList():
    title = "Food List"
    food_items = FoodItem.query.all()
    return render_template('menuList.html', title=title, food_items=food_items)

@app.route('/customerMenuList')
def customerMenuList():
    title = "Food List"
    food_items = FoodItem.query.all()
    return render_template('customerMenuList.html', title=title, food_items=food_items)

@app.route('/addFoodItem', methods=['GET','POST'])
def addFoodItem():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        if name and description and price:
            new_item = FoodItem(name=name, description=description, price=price)
            db.session.add(new_item)
            db.session.commit()
            return redirect(url_for('menuList'))
    return render_template('addFoodItem.html')

# create global cart object
my_cart = Cart()

# Sample data for testing
# my_cart.add(cartItem("Laptop", "ID123", 1200.00, 1))
# my_cart.add(cartItem("Phone", "ID124", 800.00, 2))
# my_cart.add(cartItem("Phone", "ID124", 800.00, 2))
# my_cart.add(cartItem("fuel", "ID126", 1.577, 3.45, "fuel"))

# Route for displaying the cart page
@app.route('/cart', methods=['GET'])
def cart():
    return render_template('cart.html', cart=my_cart.cart_list)

# Route to update item quantity in the cart
@app.route('/cart/update_quantity', methods=['POST'])
def update_quantity():
    item_name = request.form.get('item_name')
    new_quantity = request.form.get('quantity')
    item_type = request.form.get('item_type')

    if item_type == "fuel":
        new_quantity = float(new_quantity)
    else:
        new_quantity = int(new_quantity)
    
    my_cart.update(item_name, new_quantity)
    
    return redirect(url_for('cart'))

# Route to remove an item from the cart
@app.route('/cart/remove_item', methods=['POST'])
def remove_item():
    item_name = request.form.get('item_name')
    print(item_name)
    my_cart.remove(item_name)
    
    return redirect(url_for('cart'))

@app.route('/addToCart', methods=['POST'])
def addToCart():
    item_type = request.form.get('item_type')
    
    if item_type == "food":
        item_id = request.form.get('item_id')
        item = FoodItem.query.get_or_404(item_id)
        new_cart_item = cartItem(item.name, item.id, item.price, 1, itemType='Food')
        my_cart.add(new_cart_item)
        return redirect(url_for('customerMenuList'))

    elif item_type == "petrol":
        fuel_id = request.form.get('fuel')
        litres = request.form.get('litres')
        petrol = Petrol.query.get_or_404(fuel_id)
        new_cart_item = cartItem(petrol.name, petrol.id, petrol.price, int(litres), itemType='fuel')
        my_cart.add(new_cart_item)
        return redirect(url_for('customerStoresDisplay'))

    else:
        return redirect(url_for('cart'))

@app.route('/pumpAndPay', methods=['GET', 'POST'])
def pumpAndPay():
    if request.method == 'POST':
        store_id = request.form['input-code']
        return redirect(url_for('customerStoreDetails', store_id = store_id))
    return render_template('PumpAndpayPage.html')

@app.route('/choiceOfOperation')
def choiceOfOperation():
    return render_template('FuelProcessPage.html')

@app.route('/receipt', methods=['GET', 'POST'])
def receiptPage():
    if not my_cart.cart_list:
        return redirect(url_for('cart'))
    
    total_price = 0
    items = []

    for item in my_cart.cart_list:
        quantity = item._quantity
        item_total = item._price * quantity
        total_price += item_total
        items.append({
            'name': item._itemName,
            'price': item._price,
            'totalPrice': item_total,
            'quantity': quantity,
        })

    return render_template("receipt.html", total_price = total_price, items = items)

    # payment = Payment(balance=100000)
    # orders = [
    #     Order(name="hot dog", price=4.99, quantity=3),
    #     Order(name="fuel", price=70.63, quantity=1),
    #     Order(name="milk shake", price=2.30, quantity=2),
    #     Order(name="donut", price=2.99, quantity=2)
    # ]

    # for order in orders:
    #     payment.add_item(order)

    # receipt = payment.initiate_transaction()
    # total_price = receipt['totalPrice']
    # items = receipt['items']

    # #used to save point for buying prodcuts.
    # # userPoint = total_price
    # # user.addPoints(userPoint)

    # return render_template("receipt.html", total_price=total_price, items=items)

