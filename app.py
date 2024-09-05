from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from backendFiles.Authenticator import *


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
    
class Petrol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Name %s, Price %s>' % (self.name, self.price)
    
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET','POST']) 
def login():
    
    if request.method == "POST":
        username= request.form.get('name')
        password= request.form.get('name')

        try:
            auth = Authenticator()
            auth.fillData()
            user = auth.login(username, password)
            print(user) #testing
            return redirect(url_for('home', user=user))
        except:
             return render_template('login.html')
        
    
    return render_template('login.html')

@app.route('/home', methods=['GET','POST']) 
def home(user):
    
    # return redirect(url_for('home'))
    
    return render_template('home.html')