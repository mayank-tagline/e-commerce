from flask import Blueprint,session,redirect,url_for,render_template,request
from ..models.product import Product
from ..models.user import User
from ..models.user_product import UserProduct


filter_bp = Blueprint('filter',__name__)

@filter_bp.route('/search')
def search():

    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    username = session.get('user')
    user = User.query.filter_by(username= username).first()

    query = Product.query
    products = query.order_by(Product.id.desc()).all()


    liked_products = [p.product_id for p in UserProduct.query.filter_by(user_id=user.id).all()]

    product_list = []
    for p in products:
        product_list.append({
            "id": p.id,
            "name": p.product_name,
            "price": p.product_price,
            "image":p.product_image,
            "details":p.product_details,
            "category":p.product_category,
            "gender":p.product_gender,
            "stock":p.product_stock,
            "sellerId":p.seller_id
        })
    
    return render_template('search.html' ,user = user, products = products, products_json = product_list, liked_products = liked_products)



@filter_bp.route('/filter')
def filter():

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    username = session.get('user')
    user = User.query.filter_by(username=username).first()

    category = request.args.get('category')
    gender = request.args.get('gender')
    price = request.args.get('price')

    query = Product.query

    if category:
        query = query.filter(Product.product_category.in_(category.split(',')))

    if gender:
        query = query.filter(Product.product_gender.in_(gender.split(',')))

    if price:
        query = query.filter(Product.product_price <= int(price))

    products = query.order_by(Product.id.desc()).all()

    liked_products = [
        up.product_id
        for up in UserProduct.query.filter_by(user_id=user.id).all()
    ]

    return render_template('filter.html', user=user, products=products , liked_products= liked_products)
