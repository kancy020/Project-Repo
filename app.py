from flask import *

app = Flask(__name__)

'''not '''
@app.route("/")
def home():
    return redirect(url_for('payment_page'))

@app.route('/payment')
def payment_page():
   return render_template("paymentPage.html")


if __name__ == "__main__":
    app.run()
