#!/usr/bin/python3
"""
contains class Review
"""
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, Float

class Review(BaseModel):
    """
    Review Class
    """
    place_id = ''
    user_id = ''
    text = ''
