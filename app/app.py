from models import db
from flask_cors import CORS
from flask import Flask, jsonify, request, session, make_response
from flask_restful import Api, Resource
from models import User, db, Product, Order, OrderItem, Review, Favourite, bcrypt
from flask_migrate import Migrate
from werkzeug.exceptions import NotFound
import secrets

from datetime import timedelta
from flask_session import Session

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, support_credentials=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR']= True
app.secret_key = secrets.token_hex(16)
app.config['SESSION_TYPE'] = 'filesystem'
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_FILE_DIR'] = 'session_dir'



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
        data = request.get_json()

        name = data.get('name')
        category = data.get('category')
        description = data.get('description')
        grouping = data.get('grouping')
        imageURL = data.get('imageURL')
        price = data.get('price')
        rating = data.get('rating')

        if name and category and description and imageURL and price and rating:
            new_product = Product(
                name=name,
                imageURL=imageURL,
                description=description,
                price=price,
                category=category,
                rating=rating,
                grouping=grouping,          
            )

            db.session.add(new_product)
            db.session.commit()

            return make_response(jsonify(new_product.to_dict()),201)
        else:
            return jsonify({"error": "Incomplete product details"}), 422

    
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
        user_id = session.get('user_id')
        data = request.get_json()

        address = data.get('address')
        total_amount= data.get('total_amount')
        status = data.get('status')
        shipping_fees = data.get('shipping_fees')
        order_items = data.get('order_items')

        if address and total_amount and status and shipping_fees and order_items:
            new_order = Order(
                address=address,
                total_amount=total_amount,
                status=status,
                shipping_fees=shipping_fees,
                user_id=user_id
            )

            for item in order_items:
                new_order_item = OrderItem(
                    product_id=item.get('product_id'),
                    quantity=item.get('quantity'),
                    subTotal_amount=item.get('subTotal_amount')
                )
                new_order.order_items.append(new_order_item)

            db.session.add(new_order)
            db.session.commit()

            return new_order.to_dict(), 201
        else:
            return {"error": "Incomplete order details"}, 422

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

        response_dict = Favourite.query.filter_by(id=id).first().to_dict()

        response = make_response(
            jsonify(response_dict),
            200,
        )

        return response


api.add_resource(Index,'/', endpoint='landing')
api.add_resource(Users, '/users')
api.add_resource(UsersByID, '/users/<int:id>')
api.add_resource(LoginUser, '/login_user')
api.add_resource(SignupUser, '/signup_user')
api.add_resource(Products, '/products')
api.add_resource(ProductByID, '/products/<int:id>')
api.add_resource(Orders, '/orders')
api.add_resource(OrderByID, '/orders/<int:id>')
api.add_resource(OrderItems, '/order_items')
api.add_resource(OrderItemsByID, '/order_items/<int:id>')
api.add_resource(Reviews, '/reviews')
api.add_resource(ReviewsByUser, '/reviews/<int:id>')
api.add_resource(Favourites, '/favourites')
api.add_resource(FavouritesByUser, '/favourites/<int:id>')



if __name__ == '__main__':
    app.run(port=5555, debug=True)