from decimal import Decimal
from sqlalchemy import func, select
from database import Base, Session, engine
from models import Category, Product
from seed import fill_database

Base.metadata.create_all(engine)
fill_database()

with Session() as session:
    categories = session.scalars(select(Category)).all()
    # Задача 2: Чтение данных
    # Извлеките все записи из таблицы categories. Для каждой категории извлеките и выведите все связанные с ней продукты, включая их названия и цены.
    for category in categories:
        print(f"\nКатегория: {category.name}")
        for product in category.products:
            print(f"  {product.name} - {product.price}")

    # Задача 3: Обновление данных
    # Найдите в таблице products первый продукт с названием "Смартфон". Замените цену этого продукта на 349.99.
    smartphone = session.scalar(select(Product).where(Product.name == "Смартфон").limit(1))
    if smartphone is not None:
        smartphone.price = Decimal("349.99")
        session.commit()
        print("\nОбновлённая цена товара 'Смартфон': 349.99")

    # Задача 4: Агрегация и группировка
    # Используя агрегирующие функции и группировку, подсчитайте общее количество продуктов в каждой категории.
    counts = session.execute(select(Category.name, func
        .count(Product.id)
        .label("total_products"))
        .join(Product, Product.category_id == Category.id)
        .group_by(Category.id, Category.name)
    ).all()

    print("\nКоличество продуктов по категориям:")
    for category_name, total_products in counts:
        print(f"  {category_name}: {total_products}")

    # Задача 5: Группировка с фильтрацией
    # Отфильтруйте и выведите только те категории, в которых более одного продукта.
    filtered_categories = session.execute(
        select(Category.name)
        .join(Product, Product.category_id == Category.id)
        .group_by(Category.id, Category.name)
        .having(func.count(Product.id) > 1)
    ).all()

    print("\nКатегории с более чем одним продуктом:")
    for (category_name,) in filtered_categories:
        print(f"  {category_name}")