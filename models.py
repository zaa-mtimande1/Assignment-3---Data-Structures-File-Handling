from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, Boolean, MetaData
from db import Base

# Table definition using Table objects
metadata = MetaData()

users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("username", String(50), nullable=False, unique=True),
    Column("email", String(100), nullable=False, unique=True),
    Column("created_at", TIMESTAMP),
)

# ORM model using declarative base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    created_at = Column(TIMESTAMP)
