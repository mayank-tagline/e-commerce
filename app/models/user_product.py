from ..extensions import db

class UserProduct(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    user_id= db.Column (db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    __table_args__ = (
        db.UniqueConstraint('user_id', 'product_id',name='uq_user_product'),
    )