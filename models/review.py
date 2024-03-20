#!/usr/bin/python3
"""
contains class Review
"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlqlchemy imoprt Column, String, ForeignKey


class Review(BaseModel):
    """
    Review Class
    """
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    text = Column(String(1024), nullable=False)
