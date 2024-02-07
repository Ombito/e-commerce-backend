from models import db
from flask_cors import CORS
from flask import Flask, jsonify, request, session, make_response
from flask_restful import Api, Resource
from models import User, db, Product, Order, OrderItem, Review, Favourite, bcrypt
from flask_migrate import Migrate

from datetime import timedelta
from flask_session import Session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR']= True

db.init_app(app)
api = Api(app)
migrate = Migrate(app, db)
Session(app)

class Index(Resource):
    def get(self):
        response_body = '<h1>Hello to E-commerce server</h1>'
        status = 200
        headers = {}
        return make_response(response_body,status,headers)
    
class Users(Resource):

    def get(self):

        response_dict_list = [n.to_dict() for n in User.query.all()]

        response = make_response(
            jsonify(response_dict_list),
            200,
        )

        return response

    def post(self):

        new_record = User(
            user_id=request.form['user_id'],
            product_id=request.form['product_id'],
        )

        db.session.add(new_record)
        db.session.commit()

        response_dict = new_record.to_dict()

        response = make_response(
            jsonify(response_dict),
            201,
        )

        return response
    

class UsersByID(Resource):

    def get(self, id):

        response_dict = User.query.filter_by(id=id).first().to_dict()

        response = make_response(
            jsonify(response_dict),
            200,
        )

        return response
    
class LoginUser(Resource):
    def post(self):
        email  = request.get_json().get('email')
        password = request.get_json().get("password")

        user = User.query.filter(User.email == email).first()

        if user:
            if user.authenticate(password):
                session['user_id']=user.id
                return make_response(jsonify(user.to_dict()), 200)
                
            else:
                return make_response(jsonify({"error": "Username or password is incorrect"}), 401)
        else:
            return make_response(jsonify({"error": "User not Registered"}), 404)
        

class SignupUser(Resource):
    def post(self):
        try:
            data = request.get_json()

            full_name = data.get('full_name')
            email = data.get('email')
            phone_number = data.get('phone_number')
            password = data.get('password')

            if full_name and phone_number and email and password:
                new_user = User(full_name=full_name, phone_number=phone_number, email=email)
                new_user.password_hash = password
                db.session.add(new_user)
                db.session.commit()

                session['user_id']=new_user.id
                session['user_type'] = 'user'

                return make_response(jsonify(new_user.to_dict()),201)
            
            return make_response(jsonify({"error": "user details must be added"}),422)
    
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


class Products(Resource):

    def get(self):

        response_dict_list = [n.to_dict() for n in Product.query.all()]

        response = make_response(
            jsonify(response_dict_list),
            200,
        )
        return response

    def post(self):
        new_record = Product(
            title=request.form['title'],
            body=request.form['body'],
        )

        db.session.add(new_record)
        db.session.commit()

        response_dict = new_record.to_dict()

        response = make_response(
            jsonify(response_dict),
            201,
        )

        return response
    
class ProductByID(Resource):

    def get(self, id):
        response_dict = Product.query.filter_by(id=id).first().to_dict()

        response = make_response(
            jsonify(response_dict),
            200,
        )

        return response

class Orders(Resource):

    def get(self):

        response_dict_list = [n.to_dict() for n in Order.query.all()]

        response = make_response(
            jsonify(response_dict_list),
            200,
        )
        return response

    def post(self):
        new_record = Order(
            address=request.form['address'],
            total_amount =request.form['total_amount '],
            status=request.form['status'],
            shipping_fees=request.form['shipping_fees'],
        )

        db.session.add(new_record)
        db.session.commit()

        response_dict = new_record.to_dict()

        response = make_response(
            jsonify(response_dict),
            201,
        )

        return response

class OrderByID(Resource):

    def get(self, id):

        response_dict = Order.query.filter_by(id=id).first().to_dict()

        response = make_response(
            jsonify(response_dict),
            200,
        )

        return response


class OrderItems(Resource):

    def get(self):

        response_dict_list = [n.to_dict() for n in OrderItem.query.all()]

        response = make_response(
            jsonify(response_dict_list),
            200,
        )

        return response

    def post(self):

        new_record = OrderItem(
            title=request.form['title'],
            body=request.form['body'],
        )

        db.session.add(new_record)
        db.session.commit()

        response_dict = new_record.to_dict()

        response = make_response(
            jsonify(response_dict),
            201,
        )

        return response
    
class OrderItemsByID(Resource):

    def get(self, id):

        response_dict = OrderItem.query.filter_by(id=id).first().to_dict()

        response = make_response(
            jsonify(response_dict),
            200,
        )

        return response
    
class Reviews(Resource):

    def get(self):

        response_dict_list = [n.to_dict() for n in Review.query.all()]

        response = make_response(
            jsonify(response_dict_list),
            200,
        )

        return response

    def post(self):

        new_record = Review(
            content=request.form['content'],
            rating=request.form['rating'],
        )

        db.session.add(new_record)
        db.session.commit()

        response_dict = new_record.to_dict()

        response = make_response(
            jsonify(response_dict),
            201,
        )

        return response

class ReviewsByUser(Resource):

    def get(self, id):

        response_dict = OrderItem.query.filter_by(id=id).first().to_dict()

        response = make_response(
            jsonify(response_dict),
            200,
        )

        return response
    

class Favourites(Resource):

    def get(self):

        response_dict_list = [n.to_dict() for n in Favourite.query.all()]

        response = make_response(
            jsonify(response_dict_list),
            200,
        )

        return response

    def post(self):

        new_record = Favourite(
            user_id=request.form['user_id'],
            product_id=request.form['product_id'],
        )

        db.session.add(new_record)
        db.session.commit()

        response_dict = new_record.to_dict()

        response = make_response(
            jsonify(response_dict),
            201,
        )

        return response
    
    
class FavouritesByUser(Resource):

    def get(self, id):

        response_dict = OrderItem.query.filter_by(id=id).first().to_dict()

        response = make_response(
            jsonify(response_dict),
            200,
        )

        return response


api.add_resource(Index,'/', endpoint='landing')
api.add_resource(Users, '/users')
api.add_resource(UsersByID, '/users/<int:id>')
api.add_resource(Products, '/products')
api.add_resource(ProductByID, '/products/<int:id>')
api.add_resource(Orders, '/orders')
api.add_resource(OrderByID, '/orders/<int:id>')
api.add_resource(OrderItems, '/orderItems')
api.add_resource(OrderItemsByID, '/orderItems/<int:id>')
api.add_resource(Reviews, '/reviews')
api.add_resource(ReviewsByUser, '/reviews/<int:id>')
api.add_resource(Favourites, '/favourites')
api.add_resource(FavouritesByUser, '/favourites/<int:id>')



if __name__ == '__main__':
    app.run(port=5555, debug=True)