from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
   petrolTypes = [
   {'id': 'unleaded91', 'name': 'Unleaded 91' },
   {'id': 'unleaded95', 'name': 'Unleaded 95' },
   {'id': 'unleaded98', 'name': 'Unleaded 98' },
   {'id': 'diesel', 'name': 'Diesel' },
   {'id': 'premiumDiesel', 'name': 'Premium Diesel' },
   ]
   return render_template('PumpAndpayPage.html', petrolTypes=petrolTypes)   

if __name__ == "__main__":
   app.run(debug=True)