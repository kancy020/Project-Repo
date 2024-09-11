from flask import *

app = Flask(__name__)


@app.route("/")
def home():
    return redirect(url_for('payment_page'))

@app.route('/payment')
def payment_page():
    orders = [
        {"name": "pokemon", "quantity": 1, "price": 10.00},
        {"name": "fuel", "quantity": 1, "price": 50.00},
        {"name": "pokemon", "quantity": 1, "price": 10.00},
        {"name": "pokemon", "quantity": 1, "price": 10.00},
        {"name": "pokemon", "quantity": 1, "price": 10.00}
    ]
    return render_template("paymentPage.html", orders=orders)

@app.route('/receipt')
def receipt_page():
    # if request.method == 'POST':
    #     amount = request.form.get('amount')
    #     return render_template("receipt.html",amount=amount)
    return render_template("receipt.html")

if __name__ == "__main__":
    app.run(debug=True)
