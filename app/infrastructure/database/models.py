
from sqlalchemy import Column, Integer, String

from app.infrastructure.database.postgres import Base

class UserModel(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    email = Column(String, unique=True)

    password = Column(String)