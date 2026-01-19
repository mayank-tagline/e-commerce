from flask import Blueprint,render_template,session,redirect,url_for
from ..models.product import Product
from ..models.user import User
from ..models.user_product import UserProduct
from ..extensions import db
from ..forms import ResetPassword,UpdateUser

user_bp = Blueprint("user",__name__)



@user_bp.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    

    username = session.get('user')
    user = User.query.filter_by(username= username).first()
    return render_template('profile.html' , user = user)




@user_bp.route('/resetpassword',methods = ['GET','POST'])
def resetpassword():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
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
            return redirect(url_for('user.profile'))
        return " password is wrong!"

    username = session.get('user')
    user = User.query.filter_by(username= username).first()
    return render_template('resetpassword.html',form = form , user = user)



@user_bp.route('/updateuser', methods = ['GET','POST'])
def updateuser():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
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
        return redirect(url_for('user.profile'))

    return render_template('updateuser.html',user= user, form = form )


