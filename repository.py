from typing import TypeVar, Generic, Optional
from sqlalchemy.orm import Session , joinedload
from sqlalchemy import desc


from datetime import datetime, timedelta
from jose import JWTError, jwt
from config import SECRET_KEY, ALGORITHM

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
from model import Product , Users
import pdb



T = TypeVar("T")


class BaseRepo:
    """
    CRUD
    C = Create
    R = Read
    U = update
    D = Delete
    """
    @staticmethod
    def retrieve_all(db: Session, model: Generic[T]):
        return db.query(model).all()
    #orderby / offset / limit
    @staticmethod
    def retrieve_all_product(db: Session, model: Generic[T],limit:int,skip:int):
        sql =  db.query(model).order_by(desc(model.productname)).offset(skip).limit(limit).all()
        return sql
  
    
    @staticmethod
    def get_all_table(db: Session,Product:Product,Users:Users):
       sql =  db.query(Product,Users).join(Users).all()
       return sql
    
    @staticmethod
    def retrieve_by_id(db: Session, model: Generic[T], id: int):
        return db.query(model).filter(model.id == id).all()

    @staticmethod
    def delete_by_id(db: Session, model: Generic[T], id: int):
        return db.query(model).filter(model.product_id == id).first()
    
    @staticmethod
    def delete_by_name(db: Session, model: Generic[T],productname: str):
        return db.query(model).filter(model.productname == productname).first()
    
    @staticmethod
    def update_by_id(db: Session, model: Generic[T],price: str,id:int):
        sql =  db.query(model).filter(model.id == id).first()
        sql.price = price
        return sql
    
    @staticmethod
    def update_all(db: Session, model: Generic[T],price: str,id:int ,productname:str ,desc:str ,owner:int):
        sql =  db.query(model).filter(model.id == id).first()
        sql.price = price
        sql.productname = productname
        sql.desc = desc
        sql.owner = owner

        return sql
    

    @staticmethod
    def insert(db: Session, model: Generic[T]):
        db.add(model)
        db.commit()
        db.refresh(model)

    @staticmethod
    def update(db: Session, model: Generic[T]):
        db.commit()
        db.refresh(model)

    @staticmethod
    def delete(db: Session, model: Generic[T]):
        db.delete(model)
        db.commit()


class UsersRepo(BaseRepo):
    @staticmethod
    def find_by_username(db: Session, model: Generic[T], username: str):
        return db.query(model).filter(model.username == username).first()


class JWTRepo:
    def generate_token(data: dict, expires_delta: Optional[timedelta] = None):
        """
        to_encode = {
            "id": user_id,
            "sub": user_name,
            "exp": expire
        }
        """
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({"exp": expire})

        encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encode_jwt

    def decode_token(token: str):
        try:
            decode_token = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])
            return decode_token if decode_token["expires"] >= datetime.time() else None
        except:
            return {}


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication sheme."
                )
            if self.verfity_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expiredd token."
                )
            return credentials.credentials
        else:
            raise HTTPException(status=403, detail="Invalid authorization code.")

    def verfity_jwt(Self, jwttoken: str):
        isTokenValid: bool = False

        try:
            payload = jwt.decode(jwttoken, SECRET_KEY, algorithm=[ALGORITHM])
        except:
            payload = None

        if payload:
            isTokenValid = True
        return isTokenValid
