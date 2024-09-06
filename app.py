from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stores.db'
# Initalise DB
db = SQLAlchemy(app)

# create db model
class Stores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
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
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/addStore', methods=['GET','POST'])
def addStore():
    if request.method == "POST":
        name = request.form.get('name')
        address = request.form.get('address')
        if name and address:
            new_store = Stores(name=name, address=address)
            db.session.add(new_store)
            db.session.commit()
            return redirect(url_for('storesDisplay'))
    return render_template('addStore.html')

@app.route('/storesDisplay')
def storesDisplay():
    title = "Store List"
    stores = Stores.query.all()
    return render_template("storesDisplay.html", title=title, stores=stores)

@app.route('/storeDetails/<int:store_id>')
def storeDetails(store_id):
    store = Stores.query.get_or_404(store_id)
    return render_template('storeDetails.html', store=store)

@app.route('/addPetrol/<int:store_id>', methods=['GET', 'POST'])
def addPetrol(store_id):
    store = Stores.query.get_or_494(store_id)

    if len(store.petrols) > 3:
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

@app.route('/petrolPrices')
def petrolPrices():
    title = "Petrol Prices"
    petrol_list = Petrol.query.all()
    return render_template('petrolPrices.html', title=title, petrol_list=petrol_list)

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