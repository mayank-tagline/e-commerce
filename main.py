from flask import Flask, render_template, request, redirect, url_for, flash ,session
from flask_sqlalchemy import SQLAlchemy 
from werkzeug.utils import secure_filename
from forms import LoginForm ,RegisterForm ,AddProduct
import os


app = Flask(__name__)

app.secret_key = "tagline"

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Product(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    product_name = db.Column(db.String(100))
    product_price= db.Column(db.Integer)
    product_image= db.Column(db.String(200))
    product_details = db.Column(db.Text)
    product_category = db.Column(db.String(100))
    product_gender= db.Column(db.String(20))
    product_stock= db.Column(db.Integer)
    # product_seller = db.Column(db.Integer)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_type = db.Column(db.String(20))
    username= db.Column(db.String(100), unique = True)
    password = db.Column(db.String(100))
    

class UserProduct(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    user_id= db.Column (db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))





@app.route('/')
def main():
    if 'user' in session:
        return redirect(url_for('home'))
    # if 'user' not in session:
    #     return redirect(url_for('login'))
    
    # username = session.get('user')
    # user = User.query.filter_by(username= username).first()

    return render_template("main.html" )


@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    username = session.get('user')
    user = User.query.filter_by(username= username).first()

    seller_id = user.id

    if user.user_type == 's':
        products = Product.query.filter_by(seller_id =seller_id).all()
        return render_template("home.html",user = user , products = products)
    
    else:
        products = Product.query.all()
        return render_template("home.html", user = user , products = products)
       



@app.route('/login',methods = ['GET','POST'])
def login():
    if 'user' in session:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            username= form.username.data,
            password = form.password.data
        ).first()
        if user:
            session["user"] = user.username
            return redirect(url_for("home"))
        else:
            flash("Invalid Username or password")

    return render_template("login.html", form= form)


@app.route('/register', methods =['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        exist = User.query.filter_by(username = form.username.data).first()
        if exist:
            flash("username already exist!")
            return render_template("register.html" , form = form)
        
        user = User(
            user_type = form.user_type.data,
            username = form.username.data,
            password = form.password.data
        )

        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html" , form = form)


@app.route('/addproduct/<seller_id>', methods = ['GET', 'POST'])
def addproduct(seller_id):
    form = AddProduct()
    form.product_seller_id.data = seller_id
    if form.validate_on_submit():
        # exist = Product.query.filter_by(product_name = form.product_name.data).first()
        file = form.product_image.data
        filename = secure_filename(file.filename)

        image_path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
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
        return redirect(url_for('home'))

    return render_template ('addProduct.html', form = form)


@app.route('/logout')
def logout():
    session.pop("user",None)
    return redirect(url_for('home'))


@app.route('/buy/<product_id>')
def buyButton(product_id):
    product = Product.query.filter_by(id = product_id).first()
    return render_template('buy.html', product = product)


@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)



