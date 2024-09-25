#!/usr/bin/env python3
"""User model"""

from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    A database table class named 'users'

    Columns:
        id: Integer, primary key for the table
        email: Non-nullable string with maximu length of 250 chars 
        hashed_password: Non-nullable string used to store hashed passwords
        session_id: Nullable string (optional), for tracking user sessions
        reset_token: Nullable string (optional), for password reset functionality

    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)



