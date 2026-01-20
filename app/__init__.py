from flask import Flask,render_template
from config import Config
from app.extensions import db,migrate,mail
# from .extensions import db
# import os
# from .user.home import user_bp

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app,db)
    mail.init_app(app)

    from .auth.routes import auth_bp
    from .filter.routes import filter_bp
    from .home.routes import home_bp
    from .interaction.routes import interaction_bp
    # from .models.product import Product
    # from .models.user import auth_bp
    # from .models.user_product import auth_bp
    from .payment.routes import payment_bp
    from .product.routes import product_bp
    from .user.routes import user_bp
    from .admin.routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(filter_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(interaction_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    return app

    # app.secret_key = "tagline"

    # UPLOAD_FOLDER = 'static/uploads'
    # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # app.config['SECRET_KEY'] = 'tagline'

    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    # app.config['MAIL_PORT'] = 465
    # app.config['MAIL_USERNAME'] = os.getenv("MAIL_ID")
    # app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
    # app.config['MAIL_USE_SSL'] = True
    # app.config['MAIL_USE_TLS'] = False

    # db.init_app(app)

    # app.register_blueprint(user_bp)

    # return app