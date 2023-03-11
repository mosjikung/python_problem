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
    # __table_args__ = {'schema' : 'public'}
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
    # __table_args__ = {'schema' : 'prod'}
    id = Column(Integer, primary_key=True)
    productname = Column(String)
    desc = Column(String)
    price = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    product_status_id = Column(Integer, ForeignKey("productstatus.id"))
    owner = relationship("Users", back_populates="product")
    status = relationship("Productstatus", back_populates="productx")


class Productstatus(Base):
    __tablename__ = "productstatus"
    # __table_args__ = {'schema' : 'prod'}
    id = Column(Integer, primary_key=True)
    status_name = Column(String)
    productx = relationship("Product", back_populates="status")


# model คือตัวแทน Table
