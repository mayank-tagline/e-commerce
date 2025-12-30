from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField ,SelectField
from wtforms.validators import DataRequired , InputRequired , NumberRange
from flask_wtf.file import FileField, FileRequired , FileAllowed


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators= [DataRequired()])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    user_type =  SelectField(
        'Choose an buyer/seller',
        choices=[('b', 'buyer'), ('s', 'seller')],
        validators=[InputRequired()]
    )
            # selected_select_option = form.option_select.data
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators= [DataRequired()])
    submit = SubmitField("Register")

class AddProduct(FlaskForm):
    product_name = StringField("Product Name",validators=[DataRequired()])
    product_price = IntegerField("Product Price", validators = [DataRequired(),NumberRange(min=1,message="product price must be more than 1.")])
    product_image = FileField("Upload Product Photo ", validators= [FileRequired(),FileAllowed(['jpg','jpeg','png'])])
    product_details = StringField("Product Details ", validators=[DataRequired()])
    
    product_category = SelectField('Category',
        choices=[
            ('shirt', 'Shirt'),
            ('pant', 'Pant'),
            ('shoes', 'Shoes')
        ],
        validators=[InputRequired()]
    )
    product_gender = SelectField('gender',
        choices=[
            ('men', 'Men Clothing'),
            ('women', 'Women Clothing'),
            ('kids', 'Kids Clothing')
        ],
        validators=[InputRequired()]
    )
    product_stock = IntegerField("Product stock ", validators= [DataRequired(),NumberRange(min=1,message="minimum 1 product available in stock")])
    product_seller_id = IntegerField("Product seller id ", validators= [DataRequired()])
    submit = SubmitField("Add your Product")

