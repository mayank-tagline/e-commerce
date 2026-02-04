from flask import Blueprint,session,redirect,url_for,render_template,flash
from ..models.product import Product
from ..models.user import User
from ..models.order import Order

from ..extensions import db,socketio


payment_bp = Blueprint('payment',__name__)

@payment_bp.route('/buy/<int:product_id>')
def buyButton(product_id):

    if 'user' not in session:
        return redirect(url_for('auth.login'))
    try:
        product = Product.query.filter_by(id = product_id).first()
        if product.status != 'active':
            # flash("Product is no longer available", "error")
            return render_template('product_not_found.html',status='block')
    except Exception as e:
        return render_template('product_not_found.html', error = e)

    
    # if not product:
    #     flash("no product with this id")
    #     return render_template('product_not_found.html')

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
        product_name=product.product_name,
        product_image=product.product_image,
        product_category=product.product_category,
        product_gender=product.product_gender,
        seller_id=product.seller_id,
        quantity=1,
        purchase_price=product.product_price
    )
    db.session.add(order)

    product.product_stock -= 1

    db.session.commit()
    socketio.emit("order_created",{
        "order_id": order.id,
        "quantity":order.quantity,
        "purchase_price":order.purchase_price,
        "product":{
                    "id":product.id,
                    "name":product.product_name,
                    "current_price": product.product_price,
                    "category": product.product_category,
                    "gender": product.product_gender,
                    "stock": product.product_stock,
                    "seller_id": product.seller_id,
                    "image": product.product_image,
                    },
        "user_id":user.id,
    })


    session.pop('buy_product_id', None)
    return render_template('success.html')
