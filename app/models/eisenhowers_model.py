from app.configs.database import db
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship, validates
from dataclasses import dataclass
from marshmallow import Schema, fields


class EisenhowerSchema(Schema):
    type = fields.Str()


class EisenhowersModel(db.Model):
    __tablename__ = "eisenhowers"

    id = Column(Integer, primary_key=True)
    type = Column(String(100))
