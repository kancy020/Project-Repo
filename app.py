from flask import *
from payment import *

app = Flask(__name__)


@app.route("/")
def home():
    return redirect(url_for('payment_page'))

@app.route('/payment')
def payment_page():
    return render_template("paymentPage.html")

@app.route('/receipt')
def receipt_page():

    payment = Payment(balance=100000)
    orders = [
        {"name": "pokemon", "quantity": 1, "price": 10.00},
        {"name": "fuel", "quantity": 1, "price": 50.00},
        {"name": "donut", "quantity": 2, "price": 3.99},
        {"name": "hot dog", "quantity": 1, "price": 10.00},
        {"name": "milk shake", "quantity": 3, "price": 5.00}
    ]

    return render_template("receipt.html",orders=orders)

if __name__ == "__main__":
    app.run(debug=True)
