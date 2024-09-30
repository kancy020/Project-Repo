from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from cart import cart
from items_cart import cartItem

app = Flask(__name__)

# Route for displaying the cart page
@app.route('/cart', methods=['GET'])
def view_cart():
    return render_template('cart.html', cart=my_cart.cart_list)

# Route to update item quantity in the cart
@app.route('/cart/update_quantity', methods=['POST'])
def update_quantity():
    item_id = request.form.get('item_id')
    new_quantity = int(request.form.get('quantity'))
    
    for item in my_cart.cart_list:
        if item._itemID == item_id:
            item._quantity = new_quantity  # Update the quantity
            break
    
    return redirect(url_for('view_cart'))

# Route to remove an item from the cart
@app.route('/cart/remove_item', methods=['POST'])
def remove_item():
    item_id = request.form.get('item_id')
    print(item_id)
    my_cart.remove(item_id)
    
    return redirect(url_for('view_cart'))

if __name__ == '__main__':
    app.run(debug=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stores.db'
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
    return render_template('index.html')

@app.route('/customerIndex')
def customerIndex():
    return render_template('customerIndex.html')

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

@app.route('/customerStoreDetails/<int:store_id>')
def customerStoreDetails(store_id):
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
        if new_name:
            store.name = new_name
            db.session.commit()
            return redirect(url_for('storesDisplay'))

    return render_template('editStore.html', store=store)