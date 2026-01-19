from flask import Blueprint,session,redirect,url_for,render_template,flash
from ..models.product import Product
from ..models.user import User
from ..models.order import Order

from ..extensions import db


payment_bp = Blueprint('payment',__name__)

@payment_bp.route('/buy/<int:product_id>')
def buyButton(product_id):

    if 'user' not in session:
        return redirect(url_for('auth.login'))
    product = Product.query.filter_by(id = product_id).first()

    session['buy_product_id'] = product.id

    return render_template('buy.html', product = product)



@payment_bp.route('/payment')
def payment():

    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    product_id = session.get('buy_product_id')
    if not product_id:
        return redirect(url_for('home.home'))

    product = Product.query.get_or_404(product_id)
    return render_template('payment.html',product_price = product.product_price, product = product)



@payment_bp.route('/success')
def success():

    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    product_id = session.get('buy_product_id')
    if not product_id:
        return redirect(url_for('home.home'))

    username = session.get('user')
    user = User.query.filter_by(username=username).first()

    product = Product.query.get_or_404(product_id)

    if product.product_stock <= 0:
        flash("Product out of stock")
        return redirect(url_for('home.home'))

    order = Order(
        user_id=user.id,
        product_id=product.id,
        quantity=1
    )

    product.product_stock -= 1

    db.session.add(order)
    db.session.commit()

    session.pop('buy_product_id', None)
    return render_template('success.html')
