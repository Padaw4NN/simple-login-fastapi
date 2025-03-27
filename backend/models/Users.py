import sqlalchemy
from backend.dependencies.database import Base


class Users(Base):
    __tablename__ = "users"
    #id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    username = sqlalchemy.Column(sqlalchemy.String, index=True)
    password = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
    email    = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)