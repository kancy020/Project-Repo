from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///menu.db'
db = SQLAlchemy(app)

#create db model
class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.id
    

dish = []

@app.route('/')
def menu():
    food_items = [
        {'name': 'Pizza', 'description': 'Delicious cheese pizza with a crispy crust.', 'price': '$8.99'},
        {'name': 'Burger', 'description': 'Juicy beef burger with fresh lettuce and tomato.', 'price': '$6.99'},
        {'name': 'Pasta', 'description': 'Creamy Alfredo pasta with grilled chicken.', 'price': '$7.99'},
        {'name': 'Salad', 'description': 'Fresh garden salad with a variety of veggies.', 'price': '$4.99'},
    ]
    return render_template('food.html', food_items=food_items)

@app.route('/dish/<int:menu_id>')
def dish(menu_id):
    title = "Menu"
    return render_template('dish.html', title=title)

if __name__ == '__main__':
    app.run(debug=True)
