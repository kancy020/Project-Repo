from flask import Flask, render_template

app = Flask(__name__)

@ app.route("/choises")
def petrolStationHome():
   return render_template("FuelProcessPage.html")

@ app.route("/petrolSelect")
def petrolPage():
   return render_template("PumpAndPayPage.html")

@app.route("/pay")
def payPage():
   return render_template("PayBeforePumpPage.html")

@app.route("/")
def index():
   petrolTypes = [
   {'id': 'unleaded91', 'name': 'Unleaded 91', "price": '1.30'},
   {'id': 'unleaded95', 'name': 'Unleaded 95', "price": '1.42'},
   {'id': 'unleaded98', 'name': 'Unleaded 98', "price": '1.60' },
   {'id': 'diesel', 'name': 'Diesel', "price": '1.40' },
   {'id': 'premiumDiesel', 'name': 'Premium Diesel', "price": '1.55' },
   ]
   return render_template('PumpAndpayPage.html', petrolTypes=petrolTypes)   

if __name__ == "__main__":
   app.run(debug=True)