from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    PrimaryKeyConstraint,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from config import Base
import datetime


class Users(Base):
    __tablename__ = "users"
    #   __table_args__ = (
    #       PrimaryKeyConstraint('id', name='countries_pkey'),
    #       {'schema': 'system'}
    #  )

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    phone_number = Column(String)

    first_name = Column(String)
    last_name = Column(String)

    create_date = Column(DateTime, default=datetime.datetime.now())
    update_date = Column(DateTime)

    product = relationship("Product", back_populates="owner")


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    productname = Column(String)
    desc = Column(String)
    price = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("Users", back_populates="product")


# model คือตัวแทน Table
