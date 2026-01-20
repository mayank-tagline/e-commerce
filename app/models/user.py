from ..extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_type = db.Column(db.String(20))
    username= db.Column(db.String(100), unique = True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    
    status = db.Column(
        db.String(10),
        nullable=False,
        default='active'
    )
    __table_args__ = (
        db.UniqueConstraint('email', name='uq_user_email'),
    )