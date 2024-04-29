from sqlalchemy_serializer import SerializerMixin
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint


db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone_number = db.Column(db.String(150))
    address = db.Column(db.String())
    _password_hash = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


    @hybrid_property
    def password_hash(self):
        raise AttributeError("Not allowed")

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode("utf-8"))
    
    orders = relationship('Order', backref='user', lazy=True)
    favourites = relationship('Favourite', backref='user', lazy=True)
    payments = relationship('Payment', backref='user', lazy=True)

    serialize_rules = ('-password_hash', '-orders.user', '-favourites.user', '-payments.user')
                            


class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    image_url = db.Column(db.String())
    description = db.Column(db.String())
    price = db.Column(db.Integer)
    category = db.Column(db.String(), nullable=False)
    rating = db.Column(db.Integer)
    grouping = db.Column(db.String)
    quantity = db.Column(db.Integer)

    reviews = relationship('Review', backref='reviewed_product', lazy=True)
    orders = relationship('OrderItem', backref='product', lazy=True)
    
    serialize_rules = ('-reviews.reviewed_product', '-orders.product')


class Order(db.Model, SerializerMixin):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String())
    order_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Integer)
    status = db.Column(db.String(100), nullable=False)
    shipping_fees = db.Column(db.Integer)

    order_items = relationship('OrderItem', backref='order', lazy=True)

    serialize_rules = ('-order_items.order',)


class OrderItem(db.Model, SerializerMixin):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer)
    subtotal_amount = db.Column(db.Integer)

    serialize_rules = ('-order.product', '-product.orders')


class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    rating = db.Column(db.Integer)
    product = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    serialize_rules = ('-product.reviews', '-user.favourites', '-user.orders')


class Favourite(db.Model, SerializerMixin):
    __tablename__ = 'favourites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    __table_args__ = (
        UniqueConstraint('user_id', 'product_id'),
    )

    serialize_rules = ('-user.orders', '-product.reviews')

class Payment(db.Model, SerializerMixin):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    mpesa_number = db.Column(db.String(150))
    amount = db.Column(db.Integer)
    payment_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(100))


class Newsletter(db.Model, SerializerMixin):
    __tablename__ = 'newsletters'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)

