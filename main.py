from flask import Flask, render_template, request, redirect, url_for, flash ,session , jsonify
from flask_sqlalchemy import SQLAlchemy 
from werkzeug.utils import secure_filename
from forms import LoginForm ,RegisterForm ,AddProduct,UpdateProduct,ResetPassword, UpdateUser , ForgotPassword ,OtpPage , ChangePassword
from flask_migrate import Migrate
import os
import random
from flask_mail import Mail,Message
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

app.secret_key = "tagline"

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SECRET_KEY'] = 'tagline'


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv("MAIL_ID")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app,db)

mail = Mail(app)



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
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    __table_args__ = (
        db.UniqueConstraint('email', name='uq_user_email'),
    )
    

class UserProduct(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    user_id= db.Column (db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    __table_args__ = (
        db.UniqueConstraint('user_id', 'product_id',name='uq_user_product'),
    )





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
    products = Product.query.all()

    liked_products=[]
    liked_products = [
        up.product_id for up in UserProduct.query.filter_by(user_id = user.id).all()
    ]
    

   

    # if user.user_type == 's':
    #     products = Product.query.filter_by(seller_id =seller_id).all()
    #     return render_template("home.html",user = user , products = products)
    
    # else:
    return render_template("home.html", user = user , products = products , liked_products = liked_products)
       



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
        return redirect(url_for('myproduct'))

    return render_template ('addProduct.html', form = form)


@app.route('/logout')
def logout():
    session.pop("user",None)
    return redirect(url_for('main'))


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



@app.route('/update/<int:product_id>', methods=['GET', 'POST'])
def update(product_id):
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
                app.root_path, 'static/uploads', filename
            )
            image.save(image_path)

            product.product_image = filename

        db.session.commit()
        return redirect(url_for('home'))

    return render_template('update.html', form=form, product=product)


@app.route('/cancel')
def cancel():
    return redirect(url_for('home'))





@app.route('/delete/<int:product_id>',methods = ['POST','GET'])
def delete(product_id):
    product = Product.query.get_or_404(product_id)

    if product :
        db.session.delete(product)
        db.session.commit()

    return redirect(url_for('home'))



@app.route('/myproduct')
def myproduct():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    username = session.get('user')
    user = User.query.filter_by(username= username).first()

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

    products = query.all()

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


@app.route('/favorite',methods=['POST','GET'])
def favorite():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    username = session.get('user')
    user = User.query.filter_by(username= username).first()
    

    products = (db.session.query(Product).join(UserProduct, Product.id == UserProduct.product_id).filter(UserProduct.user_id == user.id).all())

    liked_products = [ up.product_id for up in UserProduct.query.filter_by(user_id=user.id).all()]



    return render_template('favorite.html', user = user , products = products , liked_products = liked_products)

@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    

    username = session.get('user')
    user = User.query.filter_by(username= username).first()
    return render_template('profile.html' , user = user)


@app.route('/resetpassword',methods = ['GET','POST'])
def resetpassword():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    username = session.get('user')
    user = User.query.filter_by(username= username).first()
    
    form = ResetPassword()

    if form.validate_on_submit():
        print(user.password)
        if user.password == form.password.data:
            if user.password == form.new_password.data:
                return "you can not reset the same password!"
            user.password = form.new_password.data

            db.session.commit()
            return redirect(url_for('profile'))
        return " password is wrong!"

    username = session.get('user')
    user = User.query.filter_by(username= username).first()
    return render_template('resetpassword.html',form = form , user = user)

@app.route('/updateuser', methods = ['GET','POST'])
def updateuser():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    username = session.get('user')
    user = User.query.filter_by(username= username).first()
    form = UpdateUser(obj=user)
    users = User.query.all()

    if form.validate_on_submit():

        for u in users:
            if u.email == form.email.data:
                if form.email.data == user.email:
                    break
                return "email already exist!"
            
        user.username = form.username.data
        user.email = form.email.data
        print(form.email.data)

        db.session.commit()
        session["user"] = user.username
        return redirect(url_for('profile'))

    return render_template('updateuser.html',user= user, form = form )

@app.route('/forgotpassword',methods =['GET','POST'])
def forgotpassword():
    form = ForgotPassword()
    otp = random.randint(100000,1000000)
    # print(otp)

    if form.validate_on_submit():
        
        body = f"your otp is {otp}"
        subject = "forgot password "
        receiver= form.email.data
        msg = Message(
        subject=subject,
        sender=app.config['MAIL_USERNAME'],
        recipients=[receiver]
        )
        msg.body = body

        mail.send(msg)
        print(otp)

        session['otp'] = otp
        session['email']=receiver
            
        return redirect(url_for('otppage'))
    return render_template('forgotpassword.html', form = form)

@app.route('/otppage',methods =['GET','POST'])
def otppage():
    form = OtpPage()
    otp = session.get('otp')
    print(otp)
    if form.validate_on_submit():
        if otp == int(form.otp.data):
            return redirect(url_for('changepassword'))
        else :
            return 'wrong otp'

    return render_template('otppage.html',form = form)


@app.route('/changepassword',methods =['GET','POST'])
def changepassword():
    form = ChangePassword()
    if form.validate_on_submit():
        email = session.get('email')
        user = User.query.filter_by(email = email).first()
        # print(user)
        # print(user.password)
        user.password = form.password.data

        db.session.commit()
        return redirect(url_for('login'))

    return render_template('changepassword.html',form = form )
        


@app.route('/like', methods=['POST'])
def like():
    data = request.get_json()

    username = session.get('user')
    user = User.query.filter_by(username = username).first()
    user_id = user.id

    product_id = data['product_id']
    liked = data['liked']

    record = UserProduct.query.filter_by(
        user_id=user_id,
        product_id=product_id
    ).first()

    if liked:
        if record:
            return jsonify({'status': 'already liked'})

        db.session.add(UserProduct(
            user_id=user_id,
            product_id=product_id
        ))
        db.session.commit()
        return jsonify({'status': 'liked'})

    else:
        if record:
            db.session.delete(record)
            db.session.commit()
        return jsonify({'status': 'unliked'})


@app.route('/liked-products')
def liked_products():
    username = session.get('user')
    if not username:
        return jsonify([])
        # return redirect(url_for('login'))

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify([])

    liked = UserProduct.query.filter_by(user_id=user.id).all()

    liked_ids = [lp.product_id for lp in liked]
    return jsonify(liked_ids)


@app.route('/search')
def search():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    username = session.get('user')
    user = User.query.filter_by(username= username).first()

    products = Product.query.all()


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

@app.route('/filter')
def filter():
    if 'user' not in session:
        return redirect(url_for('login'))

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

    products = query.all()
    # print(products)
    # print(products[0].product_name)

    liked_products = [
        up.product_id
        for up in UserProduct.query.filter_by(user_id=user.id).all()
    ]

    return render_template('filter.html', user=user, products=products , liked_products= liked_products)

@app.route('/extra')
def extra():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    username = session.get('user')
    user = User.query.filter_by(username=username).first()
    
    return render_template('extra.html', user=user)



if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)



