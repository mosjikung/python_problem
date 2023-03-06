from typing import Generic, Optional, TypeVar, Dict
from pydantic.generics import GenericModel
from pydantic import BaseModel, Field

T = TypeVar("T")


class Parameter(BaseModel):
    data: Dict[str, str] = None


class RequestSchema(BaseModel):
    # parameter: Parameter = Field(...) #ดึงจาก Class Parameter
    parameter: Parameter = Field(
        {
            "data": {
                "username": "",
                "email": "",
                "phone_number": "",
                "password": "",
                "first_name": "",
                "last_name": "",
            }
        }
    )


class ResponseSchema(BaseModel):
    code: str
    status: str
    message: str
    result: Optional[T] = None


class UserSigupSchema(BaseModel):
    username: str
    email: str
    phone_number: str
    password: str
    first_name: str
    last_name: str


class UserSiginSchema(BaseModel):
    username: str
    password: str


class UserBase(BaseModel):
    username: str
    email: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class ProductSchema(BaseModel):
    productname: str
    desc: str
    price: str


class ProductCreate(BaseModel):
    pass


class ProductBase(ProductSchema):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    product: list[ProductBase]

    class Config:
        orm_mode = True


class DeleteProduct(BaseModel):
    product_id: int


class DeleteNameProduct(BaseModel):
    productname: str


class Userproductjoin(BaseModel):
    owner: str


class UpdatePrice(BaseModel):
    id: int
    price: str


class UpdateAllProduct(BaseModel):
    id: int
    price: str
    productname: str
    owner: str
    desc: str


# หน้า schema คือ Request Body
