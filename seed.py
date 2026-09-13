import random
from decimal import Decimal

from database import Base, engine, Session
from models import Product, Category


Base.metadata.create_all(engine)


with Session() as session:

    categories = [
        Category(
            name="Ноутбуки",
            description="Ноутбуки и компьютеры"
        ),
        Category(
            name="Смартфоны",
            description="Мобильные телефоны"
        ),
        Category(
            name="Аксессуары",
            description="Компьютерные аксессуары"
        )
    ]

    session.add_all(categories)

    products = [
        Product(
            name=f"Product {i}",
            price=Decimal(random.randint(1000, 200000)) / 100,
            in_stock=random.choice([True, False]),
            category=random.choice(categories)
        )
        for i in range(1, 21)
    ]

    session.add_all(products)
    session.commit()

    for product in products:
        print(
            product.id,
            product.name,
            product.price,
            product.in_stock,
            product.category.name
        )