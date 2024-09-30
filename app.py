from flask import Flask, render_template, request, redirect, url_for
from cart import cart
from items_cart import cartItem

app = Flask(__name__)

# Route for displaying the cart page
@app.route('/cart', methods=['GET'])
def view_cart():
    return render_template('cart.html', cart=my_cart.cart_list)

# Route to update item quantity in the cart
@app.route('/cart/update_quantity', methods=['POST'])
def update_quantity():
    item_id = request.form.get('item_id')
    new_quantity = int(request.form.get('quantity'))
    
    for item in my_cart.cart_list:
        if item._itemID == item_id:
            item._quantity = new_quantity  # Update the quantity
            break
    
    return redirect(url_for('view_cart'))

# Route to remove an item from the cart
@app.route('/cart/remove_item', methods=['POST'])
def remove_item():
    item_id = request.form.get('item_id')
    print(item_id)
    my_cart.remove(item_id)
    
    return redirect(url_for('view_cart'))

if __name__ == '__main__':
    app.run(debug=True)