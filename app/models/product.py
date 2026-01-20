from ..extensions import db

class Product(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    product_name = db.Column(db.String(100))
    product_price= db.Column(db.Integer)
    product_image= db.Column(db.String(200))
    product_details = db.Column(db.Text)
    product_category = db.Column(db.String(100))
    product_gender= db.Column(db.String(20))
    product_stock= db.Column(db.Integer)
    status = db.Column(db.String(10),nullable=False,default='active')
    # product_seller = db.Column(db.Integer)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
