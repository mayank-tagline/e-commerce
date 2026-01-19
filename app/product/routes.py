from flask import Blueprint,session,redirect,url_for,render_template,abort,request,current_app
from ..models.product import Product
from ..models.user import User
from ..models.user_product import UserProduct
from werkzeug.utils import secure_filename
from ..forms import AddProduct,UpdateProduct
from ..extensions import db
import os



product_bp = Blueprint('product',__name__)

@product_bp.route('/addproduct/<seller_id>', methods = ['GET', 'POST'])
def addproduct(seller_id):
    username = session.get('user')
    user = User.query.filter_by(username= username).first()
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    if user.user_type !='s':
        abort(404),404
    form = AddProduct()
    form.product_seller_id.data = seller_id
    if form.validate_on_submit():
        # exist = Product.query.filter_by(product_name = form.product_name.data).first()
        file = form.product_image.data
        filename = secure_filename(file.filename)

        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'],filename)
        file.save(image_path)
        

        product = Product(
            product_name = form.product_name.data,
            product_price = form.product_price.data,

            # product_image

            product_image = filename,
            product_details = form.product_details.data,
            product_category = form.product_category.data,
            product_gender = form.product_gender.data,
            product_stock = form.product_stock.data,
            seller_id = form.product_seller_id.data
        )
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('product.myproduct'))

    return render_template ('addProduct.html', form = form)



@product_bp.route('/update/<int:product_id>', methods=['GET', 'POST'])
def update(product_id):

    username = session.get('user')
    user = User.query.filter_by(username= username).first()
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    if user.user_type not in ['s', 'admin']:
        abort(404),404

    product = Product.query.get_or_404(product_id)
    form = UpdateProduct()

    if request.method == 'GET':
        form.product_name.data = product.product_name
        form.product_price.data = product.product_price
        form.product_details.data = product.product_details
        form.product_category.data = product.product_category
        form.product_gender.data = product.product_gender
        form.product_stock.data = product.product_stock

    if form.validate_on_submit():
        product.product_name = form.product_name.data
        product.product_price = form.product_price.data
        product.product_details = form.product_details.data
        product.product_category = form.product_category.data
        product.product_gender = form.product_gender.data
        product.product_stock = form.product_stock.data

     
        if form.product_image.data:
            image = form.product_image.data
            filename = secure_filename(image.filename)

            image_path = os.path.join(
                current_app.root_path, 'static/uploads', filename
            )
            image.save(image_path)

            product.product_image = filename

        db.session.commit()
        return redirect(url_for('home.home'))

    return render_template('update.html', form=form, product=product)




@product_bp.route('/delete/<int:product_id>',methods = ['POST'])
def delete(product_id):
    username = session.get('user')
    user = User.query.filter_by(username= username).first()
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    product = Product.query.get_or_404(product_id)
    # if user.user_type !='s' and user.id != product.seller_id :
    #     return "something wrong!"
    # elif product :
    #     db.session.delete(product)
    #     db.session.commit()
    # else:
    #     return "yo!"

# Admin can delete any product
    if user.user_type == 'admin':
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('admin.dashboard'))

    # Seller can delete only his own product
    elif user.user_type == 's' and product.seller_id == user.id:
        db.session.delete(product)
        db.session.commit()

    else:
        abort(403)


    return redirect(url_for('product.myproduct'))




@product_bp.route('/myproduct')
def myproduct():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    username = session.get('user')
    user = User.query.filter_by(username= username).first()
    if user.user_type !='s':
        abort(404),404  

    seller_id = user.id


    query = Product.query.filter_by(seller_id = seller_id)
    # products = Product.query.filter_by(seller_id =seller_id).all()
    category = request.args.get('category')
    gender = request.args.get('gender')
    price = request.args.get('price')

    if category:
        query = query.filter(Product.product_category.in_(category.split(',')))

    if gender:
        query = query.filter(Product.product_gender.in_(gender.split(',')))

    if price:
        query = query.filter(Product.product_price <= int(price))

    products = query.order_by(Product.id.desc()).all()

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


    
    return render_template('myproduct.html' , user = user,products = products,products_json = product_list)

@product_bp.route('/cancel')
def cancel():

    username = session.get('user')
    user = User.query.filter_by(username= username).first()
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    if user.user_type == "admin":
        return redirect(url_for('admin.dashboard'))
    return redirect(url_for('product.myproduct'))
