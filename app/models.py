from sqlalchemy_serializer import SerializerMixin
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.hybrid import hybrid_property

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone_number = db.Column(db.Integer(50))
    _password_hash = db.Column(db.String(100), nullable=False)


    @hybrid_property
    def password_hash(self):
        raise AttributeError("Not allowed")

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode("utf-8"))