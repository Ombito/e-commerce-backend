from models import db
from flask_cors import CORS
from flask import Flask, jsonify, request, session, make_response
from flask_restful import Api, Resource
from models import User, db, Product, Order, OrderItem, Review, Favourite, Newsletter, Payment, bcrypt
from flask_migrate import Migrate
from werkzeug.exceptions import NotFound
import secrets
from sqlalchemy import and_, func
from datetime import datetime, timedelta
from flask_session import Session
from sqlalchemy.exc import IntegrityError
import jwt


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True, allow_headers=["Content-Type", "Authorization"])

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
        response_body = '<h1>Welcome to e-Commerce Server</h1>'
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
                token = jwt.encode({'user_id': user.id}, app.config['SECRET_KEY'], algorithm='HS256')
                return {'token': token}, 200
                
            else:
                return make_response(jsonify({"error": "Username or password is incorrect"}), 401)
        else:
            return make_response(jsonify({"error": "User not Registered"}), 404)


class SignupUser(Resource):
    def post(self):
        try:
            data = request.get_json()

            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            phone_number = data.get('phone_number')
            password = data.get('password')

            if first_name and last_name and phone_number and email and password:
                new_user = User(first_name=first_name, last_name=last_name, phone_number=phone_number, email=email)
                new_user.password_hash = password
                db.session.add(new_user)
                db.session.commit()

                session['user_id']=new_user.id
                session['user_type'] = 'user'

                return make_response(jsonify(new_user.to_dict()),201)
            
            return make_response(jsonify({"error": "user details must be added"}),422)
    
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


class LogoutUser(Resource):
    def delete(self):
        if session.get('user_id'):
            session['user_id']=None
            return {"message": "User logged out successfully"}
        else:
            return {"error":"User must be logged in to logout"}
        

class CheckSession(Resource):
    def get(self):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return {'error': 'Authorization header missing'}, 401

        try:
            token = auth_header.split()[1]
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = payload.get('user_id')
            if user_id:
                user = User.query.get(user_id)
                if user:
                    return user.to_dict(), 200
                else:
                    return {'error': 'User not found'}, 404
            else:
                return {'error': 'Invalid token'}, 401
        except jwt.ExpiredSignatureError:
            return {'error': 'Token has expired'}, 401
        except jwt.InvalidTokenError:
            return {'error': 'Invalid token'}, 401


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
        quantity = data.get('quantity')

        if name and category and description and image_url and price:
            new_product = Product(
                name=name,
                image_url=image_url,
                description=description,
                price=price,
                category=category,
                grouping=grouping,
                quantity=quantity,          
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
        user_id = data.get('user_id')
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
        

class MpesaExpress(Resource):
    def get(self):

        response_dict_list = [n.to_dict() for n in Payment.query.all()]

        response = make_response(
            jsonify(response_dict_list),
            200,
        )
        return response
    
    def post(self):
        user_id = session.get('user_id')
        data = request.get_json()

        amount= data.get('amount')
        mpesa_number = data.get('mpesa_number')
        status = data.get('status')

        if amount and mpesa_number:
            new_payment = Payment(
                mpesa_number=mpesa_number,
                amount=amount,
                status=status,
                user_id=user_id
            )

            db.session.add(new_payment)
            db.session.commit()

            return new_payment.to_dict(), 201
        else:
            return {"error": "Payment details not complete"}, 422

#         amount = data.get('amount')
#         phone = data.get(phone)

#         endpoint = 'https://sandbpx.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
#         access_token = getAccesstoken()
#         headers = { "Authorization" : "Bearer %s" % access_token }
#         Timestamp= datetime.now()
#         times = Timestamp.strftime("%Y%m%d%H%M%S")
#         password = "1743379" + "bfbfdbebebbb3b33b3bbbll33a33a3aaa4aa5a5a5c919" + times
#         password = base.64.b64encode(password.encode('utf-8'))

#         data = {
#             'BusinessShortCode': '17373',
#             'Password': password,
#             'Timestamp': times,
#             'TransactionType': 'CustomerPayBillOnline',
#             'PartyA': phone,
#             'PartyB': '17373',
#             'PhoneNumber': phone,
#             'CallBackURL': "my_endpoint"+ "/lnmo-callback",
#             "AccountReference": "TestPay",
#             "TransactionDesc": 'Test',
#             "Amount": amount
#         }

# class Acesstoken(Resource):
#     def incoming():
#         data = request.get_json()
#         print(data)
#         return "Ok"
    
#     def getAccessToken():
#         consumer_key = "Lkkkskkksksd8e322hkl09888ced88"
#         consumer_secret = "teluuu3nnn3098evdve"
#         endpoint = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

#         r = requests.get(endpoint, auth=HTTPBasicAuth(
#             consumer_key, consumer_secret))
#         data = r.json()
#         return data['access_token']
    

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

class Newsletter(Resource):
    def get(self):
        newsletters = Newsletter.query.all()
        return jsonify([newsletter.email for newsletter in newsletters])
   
    def post(self):
        data = request.get_json()
        email = data.get('email')
       
        if email:
            new_newsletter = Newsletter( email=email )
            
            db.session.add(new_newsletter)
            db.session.commit()

            return make_response(new_newsletter.to_dict(), 201) 
        return {"error": "Newsletter details must be added"}, 422
    
class OrdersPerMonth(Resource):
    def get(self):
        orders_data = []
        current_date = datetime.now()

        for i in range(5, -1, -1): 
            start_date = current_date - timedelta(days=i * 30)
            end_date = current_date - timedelta(days=(i - 1) * 30)
            orders_count = Order.query.filter(Order.order_date >= start_date, Order.order_date < end_date).count()
            orders_data.append({
                'month': start_date.strftime('%B'),
                'orders_count': orders_count
            })
        return jsonify(orders_data)

class TopProducts(Resource):
    def get(self):
        try:
            top_products = db.session.query(Product.name, func.count(OrderItem.id).label('num_orders')) \
                .join(OrderItem, OrderItem.product_id == Product.id) \
                .group_by(Product.name) \
                .order_by(func.count(OrderItem.id).desc()) \
                .limit(5) \
                .all()           

            response_data = [{'product_name': product_name, 'num_orders': num_orders} for product_name, num_orders in top_products]

            return {'data': response_data}, 200
        except Exception as e:
            return {'error': str(e)}, 500
        
class ProductCategories(Resource):
    def get(self):
        try:
            category_counts = db.session.query(Product.category, func.count(Product.id).label('count')) \
                .group_by(Product.category) \
                .all()

            response_data = [{'category': category, 'count': count} for category, count in category_counts]

            return {'data': response_data}, 200
        except Exception as e:
            return {'error': str(e)}, 500

class DashboardStatsResource(Resource):
    def get(self):
        try:
            total_sales = db.session.query(func.sum(Order.total_amount)).scalar() or 0
            products_sold = db.session.query(func.sum(OrderItem.quantity)).scalar() or 0
            total_earnings = db.session.query(func.sum(Order.total_amount + Order.shipping_fees)).scalar() or 0
            total_customers = User.query.count()

            dashboard_stats = [
                {
                    'label': 'Total Sales',
                    'value': f'{total_sales}',
                    'color': '#85bc2b',
                    'icon': 'FaMoneyBillAlt'
                },
                {
                    'label': 'Products Sold',
                    'value': f'{products_sold:,}',
                    'color': 'orange',
                    'icon': 'FaShoppingCart'
                },
                {
                    'label': 'Total Earnings',
                    'value': f'KES {total_earnings}',
                    'color': 'red',
                    'icon': 'FaDollarSign'
                },
                {
                    'label': 'Total Customers',
                    'value': f'{total_customers}',
                    'color': 'purple',
                    'icon': 'FaUsers'
                }
            ]

            return jsonify(dashboard_stats)
        except Exception as e:
            return {'error': str(e)}, 500
        


api.add_resource(Index,'/', endpoint='landing')
api.add_resource(LoginUser, '/login_user')
api.add_resource(SignupUser, '/signup_user')
api.add_resource(LogoutUser, '/logout_user')
api.add_resource(CheckSession, '/check_session')
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
api.add_resource(Newsletter, '/newsletters')
api.add_resource(MpesaExpress, '/pay')
api.add_resource(OrdersPerMonth, '/orders-per-month')
api.add_resource(TopProducts, '/top-products')
api.add_resource(ProductCategories, '/product-categories')
api.add_resource(DashboardStatsResource, '/dashboard-stats')

@app.before_request
def before_request():
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Credentials': 'true',
            'Content-Type': 'application/json'
        }
        return make_response('', 200, headers)
    
    
@app.errorhandler(NotFound)
def handle_not_found(e):
    response = make_response(
        "Not Found:The requested endpoint(resource) does not exist",
        404
        )
    return response
    

if __name__ == '__main__':
    app.run(port=5555, debug=True)