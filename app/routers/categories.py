from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from app.models import db, Category
from app.schemas.questions import (
    CategoryBase,
    CategoryRead,
    CategoriesList,
)
from app.schemas.errors import error_message, validation_error_response
from .utils import _get_object_or_404


categories_bp = Blueprint(
    "categories",
    __name__,
    url_prefix="/categories",
)


def _name_taken(name: str, exclude_id: int | None = None) -> bool:
    query = db.select(Category.id).where(Category.name == name)
    if exclude_id is not None:
        query = query.where(Category.id != exclude_id)
    return db.session.scalar(query) is not None


@categories_bp.route("", methods=["GET"])
def get_categories():
    """Получение списка всех категорий."""
    categories = db.session.scalars(
        db.select(Category)
    ).all()
    return jsonify(CategoriesList.dump_python(categories)), 200


@categories_bp.route("", methods=["POST"])
def create_category():
    """Создание новой категории."""
    payload = request.get_json(silent=True)

    if payload is None:
        return error_message("Invalid or missing JSON body", 400)

    try:
        category_in = CategoryBase.model_validate(payload)
    except ValidationError as exc:
        return validation_error_response(exc, 422)

    if _name_taken(category_in.name):
        return error_message(f"Category '{category_in.name}' already exists", 409)

    category = Category(name=category_in.name)
    db.session.add(category)
    db.session.commit()

    return jsonify(
        CategoryRead.model_validate(category).model_dump()
    ), 201


@categories_bp.route("/<int:category_id>", methods=["PUT"])
def update_category(category_id: int):
    """Обновление категории по ID."""
    category, error = _get_object_or_404(Category, category_id)

    if error:
        return error

    payload = request.get_json(silent=True)

    if payload is None:
        return error_message("Invalid or missing JSON body", 400)

    try:
        category_in = CategoryBase.model_validate(payload)
    except ValidationError as exc:
        return validation_error_response(exc, 422)

    if _name_taken(category_in.name, exclude_id=category_id):
        return error_message(f"Category '{category_in.name}' already exists", 409)

    category.name = category_in.name
    db.session.commit()

    return jsonify(
        CategoryRead.model_validate(category).model_dump()
    ), 200


@categories_bp.route("/<int:category_id>", methods=["DELETE"])
def delete_category(category_id: int):
    """Удаление категории по ID. Вопросы категории отвязываются (category_id = NULL)."""
    category, error = _get_object_or_404(Category, category_id)

    if error:
        return error

    db.session.delete(category)
    db.session.commit()

    return "", 204
