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

    def __repr__(self):
        return '<Name %r>' % self.id
    
@app.route('/')
def index():
    return "Welcome to Store Management"

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