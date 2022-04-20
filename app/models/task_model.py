from app.configs.database import db
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship, validates, backref
from marshmallow import Schema, fields
from app.exc.task_exc import ValueOffRangeError
from app.models.categories_model import CategorySchema
from app.models.eisenhowers_model import EisenhowerSchema


class TaskModelSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    duration = fields.Int()
    categories = fields.List(fields.Nested(CategorySchema(only=("name",))))
    classification = fields.Nested(EisenhowerSchema)

    # default order JSON
    class Meta:
        ordered = True


class TaskModel(db.Model):

    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    duration = Column(Integer)
    importance = Column(Integer)
    urgency = Column(Integer)
    eisenhower_id = Column(Integer, ForeignKey("eisenhowers.id"), nullable=False)

    categories = relationship(
        "CategoriesModel",
        secondary="task_categories",
        backref=backref("task"),
    )

    classification = relationship("EisenhowersModel")

    @validates("importance", "urgency")
    def validates_status(self, key, value):
        """
        Let the 'importance' value pass through  the validates
        to compare with 'urgency' value in second stage
        """
        if key == "urgency":
            if value not in (1, 2) or self.importance not in (1, 2):
                raise ValueOffRangeError(self.importance, value)

        return value

    @validates("name")
    def validate_name(self, key, name_to_validate):
        return str(name_to_validate).title()

    @validates("eisenhower_id")
    def validate_eisenhower(self, key, value):

        eisenhower_id = {
            "Do It First": 1,
            "Delegate It": 2,
            "Schedule It": 3,
            "Delete It": 4,
        }

        if self.importance - self.urgency == 0:
            if self.urgency == 1:
                return eisenhower_id["Do It First"]
            if self.urgency == 2:
                return eisenhower_id["Delete It"]

        if self.urgency < self.importance:
            return eisenhower_id["Delegate It"]

        return eisenhower_id["Schedule It"]
