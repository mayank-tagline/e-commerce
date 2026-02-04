from ..extensions import db

class Order(db.Model):
    id = db.Column(db.Integer,primary_key= True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)

    product_id = db.Column(db.Integer,db.ForeignKey("product.id"),nullable=True)

    product_name = db.Column(db.String(100), nullable=False)
    product_image = db.Column(db.String(200))
    product_category = db.Column(db.String(100))
    product_gender = db.Column(db.String(20))
    seller_id = db.Column(db.Integer)
    
    quantity = db.Column(db.Integer,nullable=False,default=1)

    purchase_price = db.Column(db.Integer)

    # user = db.relationship("User", backref="orders")
    # product = db.relationship("Product", backref="orders")