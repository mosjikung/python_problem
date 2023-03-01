from typing import Generic, Optional, TypeVar, Dict
from pydantic.generics import GenericModel
from pydantic import BaseModel,Field

T = TypeVar('T')


class Parameter(BaseModel):
    data: Dict[str, str] = None


class RequestSchema(BaseModel):
    #parameter: Parameter = Field(...) #ดึงจาก Class Parameter
    parameter: Parameter = Field(
            {'data': {'username' : "", 'email' : "", 'phone_number' : "", 'password': "", 'first_name': "", 'last_name': ""}}
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
       

class TokenResponse(BaseModel):
    access_token :str
    token_type: str


    
class ProductSchema(BaseModel):
    product_id:str
    productname: str
    desc: str
    price: str


class DeleteProduct(BaseModel):
    product_id:str
    
    
#หน้า schema คือ Request Body