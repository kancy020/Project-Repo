from flask import *
from payment import *

app = Flask(__name__)


@app.route("/")
def home():
    return redirect(url_for('receipt_page'))

@app.route('/payment')
def payment_page():
    return render_template("paymentPage.html")

@app.route('/receipt')
def receipt_page():

    payment = Payment(balance=100000)
    orders = [
        Order(name="hot dog", price=4.99, quantity=3),
        Order(name="fuel", price=70.63, quantity=1),
        Order(name="milk shake", price=2.30, quantity=2),
        Order(name="donut", price=2.99, quantity=2)
    ]

    for order in orders:
        payment.add_item(order)

    receipt = payment.initiate_transaction()
    total_price = receipt['totalPrice']
    items = receipt['items']

    #used to save point for buying prodcuts.
    # userPoint = 1
    # user.addPoints(userPoint)

    return render_template("receipt.html", total_price=total_price, items=items)

if __name__ == "__main__":
    app.run(debug=True)
