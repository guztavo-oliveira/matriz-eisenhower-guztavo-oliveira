from app.configs.database import db
from sqlalchemy import Column, Integer, ForeignKey

task_categories = db.Table(
    "task_categories",
    Column("id", Integer, primary_key=True),
    Column("task_id", Integer, ForeignKey("tasks.id")),
    Column("category_id", Integer, ForeignKey("categories.id")),
)
