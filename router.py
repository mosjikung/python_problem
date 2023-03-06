from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import List
from schema import (
    ProductCreate,
    RequestSchema,
    ResponseSchema,
    TokenResponse,
    UserSigupSchema,
    UserSiginSchema,
    ProductSchema,
    DeleteProduct,
    DeleteNameProduct,
    Userproductjoin,
    UpdatePrice,
    UpdateAllProduct,
    ProductBase,
)
from sqlalchemy.orm import Session
from config import get_db, ACCESS_TOKEN_EXPIRE_MINUTES
from passlib.context import CryptContext
from repository import JWTRepo, JWTBearer, UsersRepo, BaseRepo

from model import Users, Product
from datetime import datetime, timedelta
import pdb
import json


router = APIRouter()

# encrypt password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
"""
    Authentication Router
"""


@router.post("/test")
async def test(
    request: RequestSchema, db: Session = Depends(get_db)
):  # get_db->config.py
    try:
        print(request)
        return ResponseSchema(
            code="200", status="Ok", message="Success save data"
        ).dict(exclude_none=True)
    except Exception as error:
        print(error.args)
        return ResponseSchema(
            code="500", status="Error", message="Internal Server Error"
        ).dict(exclude_none=True)


@router.post("/signup")
async def signup(
    request: UserSigupSchema, db: Session = Depends(get_db)
):  # UserSignupSchema จาก Schema
    try:
        # insert user to db
        # Users จาก Model
        _user = Users(
            username=request.username,
            email=request.email,
            phone_number=request.phone_number,
            password=pwd_context.hash(request.password),
            first_name=request.first_name,
            last_name=request.last_name,
        )
        UsersRepo.insert(db, _user)
        return ResponseSchema(
            code="200", status="Ok", message="Success save data"
        ).dict(exclude_none=True)
    except Exception as error:
        print(error.args)
        return ResponseSchema(
            code="500", status="Error", message="Internal Server Error"
        ).dict(exclude_none=True)


@router.post("/login")
async def login(request: UserSiginSchema, db: Session = Depends(get_db)):
    try:
        # find user by username
        _user = UsersRepo.find_by_username(db, Users, request.username)

        if not pwd_context.verify(
            request.password, _user.password
        ):  # pwd_context เข้ารหัส
            return ResponseSchema(
                code="400", status="Bad Request", message="Invalid password"
            ).dict(exclude_none=True)

        token = JWTRepo.generate_token({"id": _user.id, "sub": _user.username})
        return ResponseSchema(
            code="200",
            status="OK",
            message="success login!",
            result=TokenResponse(access_token=token, token_type="Bearer"),
        ).dict(exclude_none=True)

    except Exception as error:
        error_message = str(error.args)
        print(error_message)
        return ResponseSchema(
            code="500", status="Internal Server Error", message="Internal Server Error"
        ).dict(exclude_none=True)


"""
    Users Router
"""


@router.get("/users", dependencies=[Depends(JWTBearer())])
async def retrieve_all(db: Session = Depends(get_db)):
    _user = UsersRepo.retrieve_all(db, Users)
    return ResponseSchema(
        code="200", status="Ok", message="Sucess retrieve data", result=_user
    ).dict(exclude_none=True)


"""
    product Router
"""


@router.get("/allproduct")
async def retrieve_all_product(limit: int, skip: int, db: Session = Depends(get_db)):
    product = BaseRepo.retrieve_all_product(db, Product, limit, skip)
    return ResponseSchema(
        code="200", status="Ok", message="Sucess retrieve data", result=product
    ).dict(exclude_none=True)


@router.post("/insert")
async def insert(request: ProductSchema, db: Session = Depends(get_db)):
    try:
        # insert user to db
        _product = Product(
            productname=request.productname,
            desc=request.desc,
            price=request.price,
            owner=request.owner,
        )
        BaseRepo.insert(db, _product)
        return ResponseSchema(
            code="200", status="Ok", message="Success save data"
        ).dict(exclude_none=True)
    except Exception as error:
        print(error.args)
        return ResponseSchema(
            code="500", status="Error", message="Internal Server Error"
        ).dict(exclude_none=True)


@router.delete("/delete")
async def delete_product_name(
    request: DeleteNameProduct, db: Session = Depends(get_db)
):
    try:
        # delete User by name

        _delete = BaseRepo.delete_by_name(db, Product, request.productname)

        BaseRepo.delete(db, _delete)
        return ResponseSchema(
            code="200", status="Ok", message="Success save data"
        ).dict(exclude_none=True)
    except Exception as error:
        print(error.args)
        return ResponseSchema(
            code="500", status="Error", message="Internal Server Error"
        ).dict(exclude_none=True)


@router.patch("/Update")
async def update(request: UpdatePrice, db: Session = Depends(get_db)):
    try:
        # delete User by name

        _update = BaseRepo.update_by_id(db, Product, request.price, request.id)

        BaseRepo.update(db, _update)
        return ResponseSchema(
            code="200", status="Ok", message="Success save data"
        ).dict(exclude_none=True)
    except Exception as error:
        print(error.args)
        return ResponseSchema(
            code="500", status="Error", message="Internal Server Error"
        ).dict(exclude_none=True)


@router.put("/UpdateAll")
async def update(request: UpdateAllProduct, db: Session = Depends(get_db)):
    try:
        # delete User by name

        _updateall = BaseRepo.update_all(
            db,
            Product,
            request.price,
            request.id,
            request.productname,
            request.desc,
            request.owner,
        )

        BaseRepo.update(db, _updateall)
        return ResponseSchema(
            code="200", status="Ok", message="Success save data"
        ).dict(exclude_none=True)
    except Exception as error:
        print(error.args)
        return ResponseSchema(
            code="500", status="Error", message="Internal Server Error"
        ).dict(exclude_none=True)


"""
    join table
"""


@router.get("/Join2table")
async def all_table(db: Session = Depends(get_db)):
    result = BaseRepo.get_all_table(db, Product, Users)
    # last_result = []
    # for username , productname , owner_id in result:
    #     last_result.append({
    #         'username':username,
    #         'productname':productname,
    #         'owner_id':owner_id
    #     })

    # return last_result
    return ResponseSchema(
        code="200", status="Ok", message="Sucess retrieve data", result=product
    ).dict(exclude_none=True)
       
        
        
@router.post("/users/{user_id}/product")
def create_item_for_user(
    user_id: int, product: ProductSchema, db: Session = Depends(get_db)
):
    product = BaseRepo.insert_product_user(db, Product, product, user_id)
    return ResponseSchema(
        code="200", status="Ok", message="Sucess retrieve data", result=product
    ).dict(exclude_none=True)