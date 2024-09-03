from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def menu():
    food_items = [
        {'name': 'Pizza', 'description': 'Delicious cheese pizza with a crispy crust.', 'price': '$8.99'},
        {'name': 'Burger', 'description': 'Juicy beef burger with fresh lettuce and tomato.', 'price': '$6.99'},
        {'name': 'Pasta', 'description': 'Creamy Alfredo pasta with grilled chicken.', 'price': '$7.99'},
        {'name': 'Salad', 'description': 'Fresh garden salad with a variety of veggies.', 'price': '$4.99'},
    ]
    return render_template('food.html', food_items=food_items)

if __name__ == '__main__':
    app.run(debug=True)
