from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, IntegerField, SelectField, DateField, SubmitField
)
from wtforms.validators import DataRequired, Email, Length, NumberRange

class RegisterForm(FlaskForm):
    name  = StringField("Shop Name",  validators=[DataRequired(), Length(max=80)])
    email = StringField("Email",      validators=[DataRequired(), Email(), Length(max=120)])
    pwd   = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email",      validators=[DataRequired(), Email()])
    pwd   = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

class DiscountForm(FlaskForm):
    product  = StringField("Product", validators=[DataRequired(), Length(max=120)])
    percent  = IntegerField("Discount %", validators=[DataRequired(), NumberRange(1, 100)])
    category = SelectField(
        "Category",
        choices=[
            ("Kitchen","Kitchen"), ("Hotel","Hotel"), ("Restaurant","Restaurant"),
            ("Electronics","Electronics"), ("Clothing","Clothing")
        ],
        validators=[DataRequired()]
    )
    start = DateField("Start Date", validators=[DataRequired()])
    end   = DateField("End Date",   validators=[DataRequired()])
    city  = StringField("City", validators=[DataRequired(), Length(max=80)])
    submit = SubmitField("Publish")
