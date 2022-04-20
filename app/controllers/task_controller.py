from http import HTTPStatus
from flask import request
from app.configs.database import db
from app.models.task_model import TaskModel, TaskModelSchema
from app.models.categories_model import CategoriesModel
from app.exc.task_exc import ValueOffRangeError
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError


def create_task():
    data = request.get_json()

    # If 'eisenhower_id is None they can't be validaded by ´validates´ decorator
    data["eisenhower_id"] = 0

    categories = data.pop("categories")
    try:
        new_task = TaskModel(**data)

        for category in categories:
            search_category = CategoriesModel.query.filter_by(name=category).first()

            if not search_category:
                new_category = CategoriesModel(name=category, description="")
                new_task.categories.append(new_category)
            else:
                new_task.categories.append(search_category)

        db.session.add(new_task)
        db.session.commit()

    except IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            return {"msg": "task already exists!"}, HTTPStatus.CONFLICT

    except ValueOffRangeError as e:
        return e.message, HTTPStatus.BAD_REQUEST

    return TaskModelSchema().dump(new_task), HTTPStatus.CREATED


def update_task(id: int):
    data = request.get_json()

    task: TaskModel = TaskModel.query.filter_by(id=id).first()

    if not task:
        return {"msg": "task not found!"}, HTTPStatus.NOT_FOUND

    try:
        for key, value in data.items():
            setattr(task, key, value)

        task.eisenhower_id = task.validate_eisenhower("", "")

        db.session.commit()

    except ValueOffRangeError as e:
        return e.message, HTTPStatus.BAD_REQUEST

    return TaskModelSchema().dump(task), HTTPStatus.OK


def delete_task(id: int):
    task: TaskModel = TaskModel.query.filter_by(id=id).first()

    if not task:
        return {"msg": "task not found!"}, HTTPStatus.NOT_FOUND

    db.session.delete(task)
    db.session.commit()

    return "", HTTPStatus.NO_CONTENT
