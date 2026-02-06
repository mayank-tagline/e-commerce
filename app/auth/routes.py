from flask import Blueprint ,session,redirect,url_for,flash,render_template,abort,current_app
from ..models.user import User
from ..forms import LoginForm ,RegisterForm,ForgotPassword,ChangePassword,OtpPage
from ..extensions import db,mail
import random
from flask_mail import Message


auth_bp = Blueprint('auth',__name__)


@auth_bp.route('/login',methods = ['GET','POST'])
def login():

    if 'user' in session:
        return redirect(url_for('home.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            username= form.username.data,
            password = form.password.data
        ).first()
        if not user:
            flash("Invalid username or password")
            return redirect(url_for('auth.login'))

        if user.status == 'block':
            flash('Your account has been blocked by admin')
            return redirect(url_for('auth.login'))

        session["user"] = user.username

        if user.user_type == "admin":
            return redirect(url_for('admin.dashboard'))

        return redirect(url_for("home.home"))

    return render_template("login.html", form= form)



@auth_bp.route('/register', methods =['GET','POST'])
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
            email = form.email.data,
            password = form.password.data
        )

        db.session.add(user)
        db.session.commit()
        return redirect(url_for("auth.login"))
    return render_template("register.html" , form = form)



@auth_bp.route('/logout')
def logout():

    session.pop("user",None)
    return redirect(url_for('home.main'))



@auth_bp.route('/forgotpassword',methods =['GET','POST'])
def forgotpassword():

    form = ForgotPassword()
    # print(otp)

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash("Email not registered")
            return render_template('forgotpassword.html', form=form)

        otp = random.randint(100000,999999)
        
        body = f"your otp is {otp}"
        subject = "forgot password "
        receiver= form.email.data
        msg = Message(
        subject=subject,
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[receiver]
        )
        msg.body = body

        mail.send(msg)
        print(otp)

        session['otp'] = otp
        session['email']=receiver
            
        return redirect(url_for('auth.otppage'))
    return render_template('forgotpassword.html', form = form)



@auth_bp.route('/otppage',methods =['GET','POST'])
def otppage():

    form = OtpPage()
    otp = session.get('otp')
    if not otp:
        abort(404)
    print(otp)
    if form.validate_on_submit():
        if otp == int(form.otp.data):
            return redirect(url_for('auth.changepassword'))
        else :
            return 'wrong otp'

    return render_template('otppage.html',form = form)



@auth_bp.route('/changepassword',methods =['GET','POST'])
def changepassword():

    form = ChangePassword()
    email = session.get('email')
    if not email:
        abort(404)
    if form.validate_on_submit():

        user = User.query.filter_by(email = email).first()
        # print(user)
        # print(user.password)
        if not user :
            return "wrong email!"
        user.password = form.password.data

        db.session.commit()
        session.pop('otp', None)
        session.pop('email', None)

        return redirect(url_for('auth.login'))

    return render_template('changepassword.html',form = form )
        

