from app.configs.database import db
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship, validates
from marshmallow import Schema, fields


class CategorySchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()

    # default order JSON
    class Meta:
        ordered = True


class CategoriesModel(db.Model):

    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
