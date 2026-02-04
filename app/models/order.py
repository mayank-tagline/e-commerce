from ..extensions import db

class Order(db.Model):
    id = db.Column(db.Integer,primary_key= True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)

    product_id = db.Column(db.Integer,db.ForeignKey("product.id", ondelete="CASCADE"),nullable=False)

    quantity = db.Column(db.Integer,nullable=False,default=1)

    purchase_price = db.Column(db.Integer)

    user = db.relationship("User", backref="orders")
    # product = db.relationship("Product", backref="orders")