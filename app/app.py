from models import db
from flask_cors import CORS
from flask import Flask, jsonify, request, session, make_response
from flask_restful import Api, Resource
from models import User, db, Product, Order, OrderItem, Review, Favourite, bcrypt
from flask_migrate import Migrate
from werkzeug.exceptions import NotFound
import secrets
from sqlalchemy import and_
from datetime import timedelta
from flask_session import Session
from sqlalchemy.exc import IntegrityError


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
    
class UserFavourite(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)

        if user:
            favourite_products = Product.query.join(Favourite).filter(Favourite.user_id == user_id).all()
            serialized_favourites = [product.to_dict() for product in favourite_products]
            return serialized_favourites
        else:
            return jsonify({'message': 'User not found'}), 404
        

class UserFavouriteByID(Resource):            
    def delete(self, user_id, product_id):
        favourite = Favourite.query.filter_by(user_id=user_id, product_id=product_id).first()
        if favourite:
            db.session.delete(favourite)
            db.session.commit()
            return {"message": "Favourite deleted successfully"}, 200
        else:
            return {"error": "Favourite not found"}, 404
        


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
        image_url = data.get('image_url')
        price = data.get('price')
        rating = data.get('rating')

        if name and category and description and image_url and price and rating:
            new_product = Product(
                name=name,
                image_url=image_url,
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
    
    def patch(self, id):
        product = Product.query.filter_by(id=id).first()

        if product:
            for attr in request.get_json():
                setattr(product,attr,request.get_json()[attr])

                db.session.add(product)
                db.session.commit()
            return make_response(jsonify(product.to_dict(), 200)) 
        
        
        return {"error": "Product record not found"}, 404
    
    def delete(self, id):
        product = Product.query.filter_by(id=id).first()
        if product:
            db.session.delete(product)
            db.session.commit()
            return {"message": "Product deleted successfully"}, 200
        else:
            return {"error": "Product not found"}, 404
    

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
                    subtotal_amount=item.get('subtotal_amount')
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
    
    def delete(self, id):
        order_item = OrderItem.query.get(id)
        if order_item:
            try:
                order = order_item.order
                if len(order.order_items) == 1:
                    db.session.delete(order) 
                db.session.delete(order_item)
                db.session.commit()
                return {"message": "Order item deleted successfully"}, 200
            except Exception as e:
                return {"error": str(e)}, 500  
        else:
            return {"error": "Order item not found"}, 404
        

    
class Reviews(Resource):

    def get(self):

        response_dict_list = [n.to_dict() for n in Review.query.all()]

        response = make_response(
            jsonify(response_dict_list),
            200,
        )

        return response

    def post(self):
        user_id = session.get('user_id')
        data = request.get_json()

        content = data.get('content')
        rating = data.get('rating')
        product = data.get('product')

        if content and rating and product:
            new_review = Review(
                content=content,
                rating=rating,
                product=product,
                user=user_id
            )

            db.session.add(new_review)
            db.session.commit()

            return make_response(jsonify(new_review.to_dict()),201)
        else:
            return jsonify({"error": "Incomplete reviewdetails"}), 422
        

class ReviewsByID(Resource):

    def get(self, id):

        response_dict = OrderItem.query.filter_by(id=id).first().to_dict()

        response = make_response(
            jsonify(response_dict),
            200,
        )

        return response
    
    def delete(self, id):
        review = Review.query.filter_by(id=id).first()
        if review:
            db.session.delete(review)
            db.session.commit()
            return {"message": "Review deleted successfully"}, 200
        else:
            return {"error": "Review not found"}, 404
    

class Favourites(Resource):

    def get(self):

        response_dict_list = [n.to_dict() for n in Favourite.query.all()]

        response = make_response(
            jsonify(response_dict_list),
            200,
        )

        return response

    def post(self):
        user_id = session.get('user_id')
        data = request.get_json()

        product_id = data.get('product_id')

        if product_id:
            new_favourite = Favourite(
                product_id=product_id,
                user_id=user_id
            )

            db.session.add(new_favourite)
            db.session.commit()

            return make_response(jsonify(new_favourite.to_dict()),201)
        else:
            return jsonify({"error": "Incomplete favourite product"}), 422
    
    
class FavouritesByID(Resource):

    def get(self, id):

        response_dict = Favourite.query.filter_by(id=id).first().to_dict()

        response = make_response(
            jsonify(response_dict),
            200,
        )

        return response
    
    def delete(self, id):
        order = Favourite.query.filter_by(id=id).first()

        if order:
            db.session.delete(order)
            db.session.commit()
            return {"message": "Favourite deleted successfully"}, 200
        else:
            return {"error": "Favourite not found"}, 404


api.add_resource(Index,'/', endpoint='landing')
api.add_resource(LoginUser, '/login_user')
api.add_resource(SignupUser, '/signup_user')
api.add_resource(Users, '/users')
api.add_resource(UsersByID, '/users/<int:id>')
api.add_resource(UserFavourite, '/users/<int:user_id>/favourites')
api.add_resource(UserFavouriteByID, '/users/<int:user_id>/favourites/<int:product_id>')
api.add_resource(Products, '/products')
api.add_resource(ProductByID, '/products/<int:id>')
api.add_resource(Orders, '/orders')
api.add_resource(OrderByID, '/orders/<int:id>')
api.add_resource(OrderItems, '/order_items')
api.add_resource(OrderItemsByID, '/order_items/<int:id>')
api.add_resource(Reviews, '/reviews')
api.add_resource(ReviewsByID, '/reviews/<int:id>')
api.add_resource(Favourites, '/favourites')
api.add_resource(FavouritesByID, '/favourites/<int:id>')



if __name__ == '__main__':
    app.run(port=5555, debug=True)