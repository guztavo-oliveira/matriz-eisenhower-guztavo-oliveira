from http import HTTPStatus
from app.configs.database import db
from app.models.categories_model import CategoriesModel, CategorySchema
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation


def create_category():
    session = db.session
    data = request.get_json()

    try:
        new_category = CategoriesModel(**data)

        session.add(new_category)
        session.commit()

    except IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            return {"msg": "category already exists!"}, HTTPStatus.CONFLICT

    schema = CategorySchema()
    result = schema.dump(new_category)

    return result, HTTPStatus.OK


def update_category(id: int):
    data = request.get_json()

    category = db.session.query(CategoriesModel).filter_by(id=id).first()

    if not category:
        return {"msg": "Category not found!"}, HTTPStatus.NOT_FOUND

    for key, value in data.items():
        setattr(category, key, value)

    db.session.add(category)
    db.session.commit()

    return CategorySchema().dump(category), HTTPStatus.OK


def delete_category(id: int):
    category = db.session.query(CategoriesModel).filter_by(id=id).first()

    if not category:
        return {"msg": "Category not found!"}, HTTPStatus.NOT_FOUND

    db.session.delete(category)
    db.session.commit()

    return "", HTTPStatus.NO_CONTENT


def retrieve_categories():
    categories: CategoriesModel = CategoriesModel.query.all()

    if not categories:
        return {"msg": "Nothing to see here, no even one category registred"}

    return jsonify(
        [
            {
                "id": category.id,
                "name": category.name,
                "description": category.description,
                "tasks": [
                    {
                        "id": task.id,
                        "name": task.name,
                        "description": task.description,
                        "duration": task.duration,
                        "classification": task.classification.type,
                    }
                    for task in category.task
                ],
            }
            for category in categories
        ]
    )
