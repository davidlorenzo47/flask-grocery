from flask_wtf import FlaskForm
from flask_wtf import validators
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User

class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField(label='User Name', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account') 

class LoginForm(FlaskForm):

    def validate_username(self,utc):
        user=User.query.filter_by(username=utc.data).first()
        if(not user):
            raise ValidationError("Username doesn't exist")

    
    username=StringField(label='Username:',validators=[DataRequired()])
    password=PasswordField(label='Password:',validators=[DataRequired()])
    submit=SubmitField(label='Login')
    
class PurchaseItemForm(FlaskForm):
    
     submit=SubmitField(label="ADD TO CART !")
     
    
    
class SellItemForm(FlaskForm):
    
     submit=SubmitField(label="REMOVE FROM CART !")
     
     
class BuyForm(FlaskForm):
    buy=SubmitField(label="BUY")
    


class AddItemForm(FlaskForm):
    item_name=StringField(label="Item Name:",validators=[DataRequired()])
    price=IntegerField(label="Price:",validators=[DataRequired()])
    submit=SubmitField(label='ADD ITEM')
    
class SetBudgetForm(FlaskForm):
    new_budget=IntegerField(label="New Budget:",validators=[DataRequired()])
    submit=SubmitField(label='Set')
