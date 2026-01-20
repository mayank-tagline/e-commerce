from flask import Blueprint,redirect,url_for,render_template,session,flash,request 
from sqlalchemy import or_
from ..models.user import User
from ..models.user_product import UserProduct
from ..models.product import Product
from ..models.order import Order

from ..extensions import db


admin_bp = Blueprint('admin',__name__,url_prefix="/admin")

def is_admin():

    username = session.get("user")
    if not username:
        return None
    user = User.query.filter_by(username=username).first()
    if not user or user.user_type != "admin":
        return None
    return user


@admin_bp.route("/")
def main():

    admin = is_admin()
    if not admin:
        session.pop("user", None)   # logout user safely
        flash("Admin access required. Please login again.", "error")
        return redirect(url_for("auth.login"))

    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/dashboard")
def dashboard():

    admin = is_admin()
    if not admin:
        return redirect(url_for("home.home"))

    products = Product.query.order_by(Product.id.desc()).all()
    users = User.query.order_by(User.id.desc()).all()

    liked_products = [
        up.product_id for up in UserProduct.query.filter_by(user_id = admin.id).all()
    ]
    
    return render_template("admin_dashboard.html",user= admin,users=users,products = products,liked_products = liked_products)


@admin_bp.route("/seller/<int:seller_id>/products")
def seller_products(seller_id):

    admin = is_admin()
    if not admin:
        return redirect(url_for("home.home"))

    products = Product.query.filter_by(seller_id=seller_id).all()
    return render_template("admin_seller_products.html", products=products)


@admin_bp.route("/buyer/<int:buyer_id>/products")
def buyer_products(buyer_id):

    admin = is_admin()
    if not admin:
        return redirect(url_for("home.home"))

    orders = Order.query.filter(Order.user_id == buyer_id).all()

    return render_template("admin_buyer_products.html",orders=orders)


@admin_bp.route("/user/update/<int:user_id>", methods=["GET", "POST"])
def update_user(user_id):
    admin = is_admin()
    if not admin:
        return redirect(url_for("home.home"))

    user = User.query.get_or_404(user_id)

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        status = request.form.get("status")

        existing_user = User.query.filter(
            User.id != user.id,
            or_(
                User.username == username,
                User.email == email
            )
        ).first()

        if existing_user:
            if existing_user.username == username:
                flash("Username already exists", "error")
            if existing_user.email == email:
                flash("Email already exists", "error")
            return redirect(url_for("admin.update_user", user_id=user.id))


        if user.user_type == "admin" and status == "block":
            flash("Admin user cannot be blocked", "error")
            return redirect(url_for("admin.update_user", user_id=user.id))

        user.username = username
        user.email = email
        user.status = status


        if user.user_type == "s" and status == "block":
            Product.query.filter_by(seller_id=user.id).update(
                {"status": "hide"}
            )

        # (optional) If seller is re-activated → show products again
        if user.user_type == "s" and status == "active":
            Product.query.filter_by(seller_id=user.id).update(
                {"status": "active"}
            )

            
        db.session.commit()
        return redirect(url_for("admin.dashboard"))

    return render_template("admin_update_user.html", user=user)


@admin_bp.route("/user/delete/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    admin = is_admin()
    if not admin:
        return redirect(url_for("home.home"))

    user = User.query.get_or_404(user_id)

    if user.user_type == "admin":
        flash("Admin user cannot be deleted")
        return redirect(url_for("admin.dashboard"))
    
    if user.user_type == "s":
        products = Product.query.filter_by(seller_id=user.id).all()
        for product in products:
            Order.query.filter_by(product_id=product.id).delete()
            db.session.delete(product)

    UserProduct.query.filter_by(user_id=user.id).delete()
    Order.query.filter_by(user_id=user.id).delete()

    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("admin.dashboard"))
