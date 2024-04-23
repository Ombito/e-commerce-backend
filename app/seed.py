from models import db, User, Product, Order, OrderItem, Review, Favourite, Newsletter
from flask_bcrypt import Bcrypt
from datetime import datetime
from app import app

bcrypt = Bcrypt()

app.app_context().push()
db.drop_all()
db.create_all()

with app.app_context():
    db.create_all()

    # Seed Users
    users_data = [
        {
            'first_name': 'Purity',
            'last_name': 'Kamau',
            'email': 'purity@gmail.com',
            'phone_number': '123456789',
            'address': 'Nairobi, Kenya',
        },
        {
            'first_name': 'Susan',
            'last_name': 'Karanja',
            'email': 'susan@gmail.com',
            'phone_number': '987654321',
            'address': 'Kiambu, Kenya',
        }
    ]

    users = []
    for user_data in users_data:
        user = User(**user_data)
        user.password_hash = bcrypt.generate_password_hash('password').decode("utf-8")
        users.append(user)
        db.session.add(user)
    db.session.commit()

    # Seed Products
    products_data = [
        {
            'name': 'Mango',
            'image_url': 'https://res.cloudinary.com/duofzxtxh/image/upload/v1709893258/mango_ayi6hj.jpg',
            'description': 'This is the description for Mango.',
            'price': 20,
            'category': 'Fruits',
            'rating': 4,
            'grouping': "trending",
            'quantity': 1,
        },
        {
            'name': 'Orange',
            'image_url': 'https://res.cloudinary.com/duofzxtxh/image/upload/v1709893260/oranges_pux073.jpg',
            'description': 'This is the description for Orange.',
            'price': 15,
            'category': 'Fruits',
            'rating': 3,
            'grouping': "trending",
            'quantity': 1,
        },
        {
            'name': 'Apple',
            'image_url': 'https://res.cloudinary.com/duofzxtxh/image/upload/v1709893258/apples_hvkv76.jpg',
            'description': 'This is the description for Apple.',
            'price': 20,
            'category': 'Fruits',
            'rating': 4,
            'grouping': "trending",
            'quantity': 1,
        },
        {
            'name': 'Banana',
            'image_url': 'https://res.cloudinary.com/duofzxtxh/image/upload/v1709893258/banana_f0cy6k.jpg',
            'description': 'This is the description for Banana.',
            'price': 15,
            'category': 'Fruits',
            'rating': 3,
            'grouping': "trending",
            'quantity': 1,
        },
        {
            'name': 'Ovacado',
            'image_url': 'https://res.cloudinary.com/duofzxtxh/image/upload/v1709893262/ovacado_lbbhzl.jpg',
            'description': 'This is the description for Banana.',
            'price': 15,
            'category': 'Fruits',
            'rating': 3,
            'grouping': "trending",
            'quantity': 1,
        },
        {
            'name': 'Pawpaw',
            'image_url': 'https://res.cloudinary.com/duofzxtxh/image/upload/v1709893263/pawpaw_rt1cun.jpg',
            'description': 'This is the description for Banana.',
            'price': 15,
            'category': 'Fruits',
            'rating': 3,
            'grouping': "trending",
            'quantity': 1,
        },
        {
            'name': 'Tea',
            'image_url': 'https://res.cloudinary.com/duofzxtxh/image/upload/v1709893271/tea_slr6il.webp',
            'description': 'This is the description for Banana.',
            'price': 15,
            'category': 'Beverages',
            'rating': 3,
            'grouping': "trending",
            'quantity': 1,
        },
        {
            'name': 'Sugarcane',
            'image_url': 'https://res.cloudinary.com/duofzxtxh/image/upload/v1709893265/sugarcane1_wtfdx5.jpg',
            'description': 'This is the description for Banana.',
            'price': 15,
            'category': 'Other produce',
            'rating': 3,
            'grouping': "trending",
            'quantity': 1,
        },
        {
            'name': 'Grapes',
            'image_url': 'https://res.cloudinary.com/duofzxtxh/image/upload/v1709893265/grapes_asxia1.jpg',
            'description': 'This is the description for Banana.',
            'price': 15,
            'category': 'Fruits',
            'rating': 3,
            'grouping': "featured",
            'quantity': 1,
        },
        {
            'name': 'Cows',
            'image_url': 'https://res.cloudinary.com/duofzxtxh/image/upload/v1709893262/beef_qraucw.webp',
            'description': 'This is the description for Banana.',
            'price': 15,
            'category': 'Meat & Poultry',
            'rating': 3,
            'grouping': "featured",
            'quantity': 1,
        },
        {
            'name': 'Eggs',
            'image_url': 'https://res.cloudinary.com/duofzxtxh/image/upload/v1709893258/eggs_v6hqmf.jpg',
            'description': 'This is the description for Banana.',
            'price': 15,
            'category': 'Meat & Poultry',
            'rating': 3,
            'grouping': "featured",
            'quantity': 1,
        },
        {
            'name': 'Mushroom',
            'image_url': 'https://res.cloudinary.com/duofzxtxh/image/upload/v1709893258/mushroom_m6gfjk.jpg',
            'description': 'This is the description for Banana.',
            'price': 15,
            'category': 'Other Produce',
            'rating': 3,
            'grouping': "trending",
            'quantity': 1,
        },
        {
            'name': 'Ovacado',
            'image_url': 'https://res.cloudinary.com/duofzxtxh/image/upload/v1709893262/ovacado_lbbhzl.jpg',
            'description': 'This is the description for Banana.',
            'price': 15,
            'category': 'Fruits',
            'rating': 3,
            'grouping': "trending",
            'quantity': 1,
        },
        {
            'name': 'Ovacado',
            'image_url': 'https://res.cloudinary.com/duofzxtxh/image/upload/v1709893262/ovacado_lbbhzl.jpg',
            'description': 'This is the description for Banana.',
            'price': 15,
            'category': 'Fruits',
            'rating': 3,
            'grouping': "trending",
            'quantity': 1,
        },
        {
            'name': 'Ovacado',
            'image_url': 'https://res.cloudinary.com/duofzxtxh/image/upload/v1709893262/ovacado_lbbhzl.jpg',
            'description': 'This is the description for Banana.',
            'price': 15,
            'category': 'Fruits',
            'rating': 3,
            'grouping': "trending",
            'quantity': 1,
        },
        {
            'name': 'Ovacado',
            'image_url': 'https://res.cloudinary.com/duofzxtxh/image/upload/v1709893262/ovacado_lbbhzl.jpg',
            'description': 'This is the description for Banana.',
            'price': 15,
            'category': 'Fruits',
            'rating': 3,
            'grouping': "trending",
            'quantity': 1,
        },
    ]

    products = []
    for product_data in products_data:
        product = Product(**product_data)
        products.append(product)
        db.session.add(product)
    db.session.commit()


    # Seed Orders
    orders_data = [
        {
            'address': 'Kisauni, Mombasa',
            'total_amount': 35,
            'status': 'Delivered',
            'shipping_fees': 25,
            'user_id': users[0].id,
        },
        {
            'address': 'Langas, Eldoret',
            'total_amount': 20,
            'status': 'Processing',
            'shipping_fees': 10,
            'user_id': users[1].id,
        },
        {
            'address': 'Kileleshwa, Nairobi',
            'total_amount': 40000,
            'status': 'Delivered',
            'shipping_fees': 35,
            'user_id': users[0].id,
        },
        {
            'address': 'Kayole, Nakuru',
            'total_amount': 155,
            'status': 'Delivered',
            'shipping_fees': 15,
            'user_id': users[1].id,
        },
        {
            'address': 'Donholm, Nairobi',
            'total_amount': 2500,
            'status': 'Delivered',
            'shipping_fees': 5,
            'user_id': users[0].id,
        },
    ]

    orders = []
    for order_data in orders_data:
        order = Order(**order_data)
        orders.append(order)
        db.session.add(order)
    db.session.commit()


    # Seed Order Items
    order_items_data = [
        {
            'order_id': orders[0].id,
            'product_id': products[0].id,
            'quantity': 2,
            'subtotal_amount': 40,
        },
        {
            'order_id': orders[1].id,
            'product_id': products[1].id,
            'quantity': 1,
            'subtotal_amount': 15,
        }
    ]

    for order_item_data in order_items_data:
        order_item = OrderItem(**order_item_data)
        db.session.add(order_item)
    db.session.commit()

    # Seed Reviews
    reviews_data = [
    {
        'content': 'Great product!',
        'rating': 5,
        'product': products[0].id,
        'user': users[0].id, 
    },
    {
        'content': 'Not bad, but could be better.',
        'rating': 3,
        'product': products[1].id, 
        'user': users[1].id, 
    }
]

for review_data in reviews_data:
    review = Review(**review_data)
    db.session.add(review)

    db.session.commit()


    # Seed Favourites
    
    favourites_data = [
        {
            'user_id': users[0].id,
            'product_id': products[1].id,
        },
        {
            'user_id': users[1].id,
            'product_id': products[0].id,
        }
    ]

    for favourite_data in favourites_data:

        existing_favourite = Favourite.query.filter_by(**favourite_data).first()
        if existing_favourite is None:
            favourite = Favourite(**favourite_data)
            db.session.add(favourite)
    db.session.commit()

    # Seed Newsletter
    newsletter = Newsletter(
        email='becky@gmail.com',
    )
    db.session.add(newsletter)
    db.session.commit()

print("Database seeded successfully")
