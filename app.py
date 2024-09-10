from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from backendFiles.Authenticator import *


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
        username = request.form.get('name')
        password = request.form.get('password')
        try:
            auth = Authenticator()
            auth.fillData()
            user = auth.login(username, password)
            
            if user!=None:
                #session['user'] = user
                return redirect(url_for('home'))
            
        except InvalidUsername:
            return render_template('login.html', error="Invalid username")
        except InvalidPassword:
            return render_template('login.html', error="Invalid password")

    return render_template('login.html')

@app.route('/signUp', methods=['GET', 'POST']) 
def signUp():
    return render_template('signUp.html')


@app.route('/home', methods=['GET', 'POST']) 
def home():

    #if 'user' in session:
    #   return render_template('home.html', user=session['user'])  # Pass user to template
    
    return render_template('home.html')