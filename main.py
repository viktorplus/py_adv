from sqlalchemy import select
from database import Session
from models import Product

with Session() as session:
    products = session.scalars(select(Product)).all()

    for product in products:
        print(
            product.id,
            product.name,
            product.price,
            product.in_stock,
            product.category.name
        )