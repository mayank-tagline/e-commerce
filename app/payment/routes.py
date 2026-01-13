from flask import Blueprint,session,redirect,url_for,render_template
from ..models.product import Product
from ..models.user import User
from ..models.user_product import UserProduct

payment_bp = Blueprint('payment',__name__)

@payment_bp.route('/buy/<product_id>')
def buyButton(product_id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    product = Product.query.filter_by(id = product_id).first()
    return render_template('buy.html', product = product)



@payment_bp.route('/payment/<int:product_price>')
def payment(product_price):
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template('payment.html',product_price = product_price)

@payment_bp.route('/success')
def success():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template('success.html')
