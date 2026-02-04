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


    orders = db.relationship(
        'Order',
        backref='product',
        cascade='all, delete-orphan',  # automatically delete orders
        passive_deletes=True
    )
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.product_name,
            "price": self.product_price,
            "image": self.product_image,
            "details": self.product_details,
            "category": self.product_category,
            "gender": self.product_gender,
            "stock": self.product_stock,
            "seller_id": self.seller_id,
            "status": self.status,
        }