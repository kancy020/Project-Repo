from flask import Flask, render_template, request, redirect, url_for
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
    title = "Food List"
    food_items = Menu.query.all()
    return render_template('food.html', title=title, food_items=food_items)

@app.route('/dish/<int:menu_id>')
def dish(menu_id):
    item = Menu.query.get_or_404(menu_id)
    return render_template('dish.html', title="Menu", item=item)

@app.route('/addItem', methods=['GET','POST'])
def addItem():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        if name and description and price:
            new_item = Menu(name=name, description=description, price=price)
            db.session.add(new_item)
            db.session.commit()
            return redirect(url_for('menu'))
    return render_template('addItem.html')

if __name__ == '__main__':
    app.run(debug=True)
