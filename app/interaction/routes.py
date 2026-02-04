from flask import Blueprint,session,redirect,url_for,render_template,request,jsonify
from ..models.product import Product
from ..models.user import User
from ..models.user_product import UserProduct

from ..extensions import db

interaction_bp = Blueprint('interaction',__name__)


@interaction_bp.route('/favorite',methods=['POST','GET'])
def favorite():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    username = session.get('user')
    user = User.query.filter_by(username= username).first()
    

    query = (db.session.query(Product).join(UserProduct, Product.id == UserProduct.product_id).filter(UserProduct.user_id == user.id))

    products = query.order_by(Product.id.desc()).all()

    liked_products = [ up.product_id for up in UserProduct.query.filter_by(user_id=user.id).all()]



    return render_template('favorite.html', user = user , products = products , liked_products = liked_products)




# @interaction_bp.route('/like', methods=['POST'])
# def like():
#     data = request.get_json()

#     username = session.get('user')
#     user = User.query.filter_by(username = username).first()
#     user_id = user.id

#     product_id = data['product_id']
#     liked = data['liked']

#     record = UserProduct.query.filter_by(
#         user_id=user_id,
#         product_id=product_id
#     ).first()

#     if liked:
#         if record:
#             return jsonify({'status': 'already liked'})

#         db.session.add(UserProduct(
#             user_id=user_id,
#             product_id=product_id
#         ))
#         db.session.commit()
#         return jsonify({'status': 'liked'})

#     else:
#         if record:
#             db.session.delete(record)
#             db.session.commit()
#         return jsonify({'status': 'unliked'})
@interaction_bp.route('/like', methods=['POST'])
def like():
    username = session.get('user')
    if not username:
        return jsonify({'error': 'unauthorized'}), 401

    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'invalid json'}), 400

    product_id = int(data.get('product_id'))
    liked = data.get('liked')

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'user not found'}), 404

    record = UserProduct.query.filter_by(
        user_id=user.id,
        product_id=product_id
    ).first()

    if liked:
        # ✅ IMPORTANT FIX
        if record:
            return jsonify({'status': 'already liked'})  # STOP here

        db.session.add(UserProduct(
            user_id=user.id,
            product_id=product_id
        ))
        db.session.commit()
        return jsonify({'status': 'liked'})

    else:
        if record:
            db.session.delete(record)
            db.session.commit()
        return jsonify({'status': 'unliked'})


@interaction_bp.route('/liked-products')
def liked_products():
    username = session.get('user')
    if not username:
        return jsonify([])
        # return redirect(url_for('login'))

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify([])

    liked = UserProduct.query.filter_by(user_id=user.id).all()

    liked_ids = [lp.product_id for lp in liked]
    return jsonify(liked_ids)
