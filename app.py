import os
from flask import Flask, render_template, redirect, url_for, session, request
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from flask_login import (login_user, login_required,
                         logout_user, UserMixin, LoginManager)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import razorpay

#  INITIALIZATION
login_manger = LoginManager()
app = Flask(__name__)
app.secret_key = 'secret'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                        os.path.join(basedir, 'foodApp.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app, db)
login_manger.init_app(app)
login_manger.login_view = 'login'
razorpay_client = razorpay.Client(auth=("rzp_test_d6KpX92YrQ9f1r",
                                        "yhiBDWq1ioUeikZ5WW3rL1T8"))


# MODELS
@login_manger.user_loader
def loader_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    address = db.Column(db.Text)

    def __init__(self, email, username, password, address):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.address = address

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Orders(db.Model, UserMixin):
    __tablename__ = 'Order'
    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer)
    email = db.Column(db.String(64))
    address = db.Column(db.Text)
    items = db.Column(db.Text)
    amount = db.Column(db.Integer)

    def __init__(self, customer_id, email, address, items, amount):
        self.customer_id = customer_id
        self.email = email
        self.address = address
        self.items = items
        self.amount = amount


# FORMS
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('LOGIN')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired(), EqualTo(
                                 'pass_confirm',
                                 message='Password must match!')])
    pass_confirm = PasswordField('Confirm Password',
                                 validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Register')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been already registered!')

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is taken!')


class Cart(FlaskForm):
    food_one = StringField()
    price_one = StringField()
    quantity_one = StringField()

    food_two = StringField()
    price_two = StringField()
    quantity_two = StringField()

    food_three = StringField()
    price_three = StringField()
    quantity_three = StringField()

    total = StringField()

    submit = SubmitField('Confirm')


# VIEWS
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None:
            if user.check_password(form.password.data):
                login_user(user)
                next_page = request.args.get('next')

                if next_page is None or next_page[0] != '/':
                    next_page = url_for('index')
                return redirect(next_page)
        else:
            return redirect(url_for('register'))

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    address=form.address.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/foodSection', methods=['GET', 'POST'])
def foodSection():
    cart = Cart()
    if cart.validate_on_submit():
        session['food_one'] = cart.food_one.data
        session['price_one'] = cart.price_one.data
        session['quantity_one'] = cart.quantity_one.data

        session['food_two'] = cart.food_two.data
        session['price_two'] = cart.price_two.data
        session['quantity_two'] = cart.quantity_two.data

        session['food_three'] = cart.food_three.data
        session['price_three'] = cart.price_three.data
        session['quantity_three'] = cart.quantity_three.data

        session['total_amount'] = cart.total.data
        session['payable_amount'] = int(cart.total.data) * 100
        return redirect(url_for('order'))
    return render_template('foodSection.html', cart=cart)


@app.route('/order')
@login_required
def order():
    return render_template('order.html')


# PAYMENT GATEWAY
@app.route('/charge', methods=['POST'])
def app_charge():
    if request.method == 'POST':
        customer_id = request.form.get('customerid')
        customer = User.query.filter_by(id=customer_id).first()

        food_one = request.form.get('food_one')
        quantity_one = request.form.get('quantity_one')

        food_two = request.form.get('food_two')
        quantity_two = request.form.get('quantity_two')

        food_three = request.form.get('food_three')
        quantity_three = request.form.get('quantity_three')

        total_amount = request.form.get('total_amount')

        item_one = food_one + "(" + quantity_one + ")" if food_one else ""
        item_two = food_two + "(" + quantity_two + ")" if food_two else ""
        item_three = food_three + "(" + quantity_three + ")" if food_three else ""

        items = item_one + item_two + item_three

        # enter above data to the database table
        place_order = Orders(customer_id, customer.email, customer.address, items, total_amount)
        db.session.add(place_order)
        db.session.commit()

    return redirect(url_for('thanks'))


@app.route('/thanks')
def thanks():
    return render_template('thanks.html')


if __name__ == '__main__':
    app.run(debug=True)
