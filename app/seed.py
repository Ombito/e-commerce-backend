from models import db, User, Product, Order, OrderItem, Review, Favourite
from flask_bcrypt import Bcrypt
from datetime import datetime
from app import app


bcrypt = Bcrypt()

app.app_context().push()
db.drop_all()
db.create_all()

with app.app_context():
    db.create_all()

    user1 = User(
        full_name='John Doe',
        email='alvin@gmail.com',
        phone_number=123456789,
        address='Nairobi, Kenya',
    )
    user1.password_hash = bcrypt.generate_password_hash('password').decode("utf-8")

    user2 = User(
        full_name='Jane Doe',
        email='joy@gmail.com',
        phone_number=987654321,
        address='Kiambu, Kenya',
    )
    user2.password_hash = bcrypt.generate_password_hash('password').decode("utf-8")

    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

   
    product1 = Product(
        name='Product 1',
        imageURL='https://example.com/product1.jpg',
        description='This is the description for Product 1.',
        price=20,
        category='Fruits',
        rating=4,
    )

    product2 = Product(
        name='Product 2',
        imageURL='https://example.com/product2.jpg',
        description='This is the description for Product 2.',
        price=15,
        category='Vegetables',
        rating=3,
    )

    db.session.add(product1)
    db.session.add(product2)
    db.session.commit()


    order1 = Order(
        address='789 Oak Street',
        total_amount=35,
        status='Delivered',
        shipping_fees=5,
        user_id=user1.id,
    )

    order2 = Order(
        address='101 Pine Street',
        total_amount=20,
        status='Processing',
        shipping_fees=0,
        user_id=user2.id,
    )

    db.session.add(order1)
    db.session.add(order2)
    db.session.commit()


    order_item1 = OrderItem(
        order_id=order1.id,
        product_id=product1.id,
        quantity=2,
        subTotal_amount=40,
    )

    order_item2 = OrderItem(
        order_id=order2.id,
        product_id=product2.id,
        quantity=1,
        subTotal_amount=15,
    )

    db.session.add(order_item1)
    db.session.add(order_item2)
    db.session.commit()


    review1 = Review(
        content='Great product!',
        rating=5,
        product=product1.id,
        user=user1.id,
    )

    review2 = Review(
        content='Not bad, but could be better.',
        rating=3,
        product=product2.id,
        user=user2.id,
    )

    db.session.add(review1)
    db.session.add(review2)
    db.session.commit()


    favourite1 = Favourite(
        user_id=user1.id,
        product_id=product2.id,
    )

    favourite2 = Favourite(
        user_id=user2.id,
        product_id=product1.id,
    )

    db.session.add(favourite1)
    db.session.add(favourite2)
    db.session.commit()
    print("Database seeded successfully")
