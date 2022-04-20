from flask import Blueprint
from app.controllers import categories_controller

bp = Blueprint("categories", __name__, url_prefix="/")

bp.post("/categories")(categories_controller.create_category)
bp.patch("/categories/<int:id>")(categories_controller.update_category)
bp.delete("/categories/<int:id>")(categories_controller.delete_category)
bp.get("")(categories_controller.retrieve_categories)
