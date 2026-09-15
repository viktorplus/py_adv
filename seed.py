from decimal import Decimal

from database import Session
from models import Category, Product


def fill_database():
    with Session() as session:
        electronics = Category(name="Электроника", description="Гаджеты и устройства.")
        books = Category(name="Книги", description="Печатные книги и электронные книги.")
        clothes = Category(name="Одежда", description="Одежда для мужчин и женщин.")

        session.add_all([electronics, books, clothes])

        products = [
            Product(name="Смартфон", price=Decimal("299.99"), in_stock=True, category=electronics),
            Product(name="Ноутбук", price=Decimal("499.99"), in_stock=True, category=electronics),
            Product(name="Научно-фантастический роман", price=Decimal("15.99"), in_stock=True, category=books),
            Product(name="Джинсы", price=Decimal("40.50"), in_stock=True, category=clothes),
            Product(name="Футболка", price=Decimal("20.00"), in_stock=True, category=clothes),
        ]

        session.add_all(products)
        session.commit()