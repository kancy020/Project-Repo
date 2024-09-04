from flask import Flask, render_template

app = Flask(__name__)

@app.route('/add_store', methods=['GET','POST'])
def add_store():
    pass

@app.route('/stores')
def list_stores():
    pass