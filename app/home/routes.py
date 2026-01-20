from flask import Blueprint ,session,redirect,url_for,render_template
from ..models.product import Product
from ..models.user import User
from ..models.user_product import UserProduct

home_bp = Blueprint('home',__name__)


@home_bp.route("/")
def main():

    if 'user' in session:
        return redirect(url_for('home.home'))

    products = Product.query.order_by(Product.id.desc()).all()

    return render_template("main.html", products = products )



@home_bp.route('/home')
def home():

    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    username = session.get('user')
    user = User.query.filter_by(username= username).first()
    products = Product.query.order_by(Product.id.desc()).all()

    liked_products=[]
    liked_products = [
        up.product_id for up in UserProduct.query.filter_by(user_id = user.id).all()
    ]
    
    return render_template("home.html", user = user , products = products , liked_products = liked_products)
       