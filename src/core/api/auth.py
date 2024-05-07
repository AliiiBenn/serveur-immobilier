from typing import Optional
from pydantic import BaseModel
from passlib.handlers.sha2_crypt import sha512_crypt as crypto

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2
from fastapi.security.oauth2 import get_authorization_scheme_param, OAuthFlowsModel
from jose import JWTError, jwt
import datetime as dt

from sqlmodel import Session, select

from .models import Compte
from .engine import Engine



# class User(BaseModel):
#     username: str
#     hashed_password: str


# # Create a "database" to hold your data. This is just for example purposes. In
# # a real world scenario you would likely connect to a SQL or NoSQL database.
# class DataBase(BaseModel):
#     user: list[User]

# DB = DataBase(
#     user=[
#         User(username="user1@gmail.com", hashed_password=crypto.hash("12345")),
#         User(username="user2@gmail.com", hashed_password=crypto.hash("12345")),
#     ]
# )

engine = Engine()


def get_user(username: str) -> Optional[Compte]:
    with Session(engine.engine) as session:
        user = session.exec(select(Compte).where(Compte.email == username)).first()
    
    print("users", user)
    return user



class Settings:
    SECRET_KEY: str = "secret-key"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  # in mins
    COOKIE_NAME = "access_token"
    
    
    
    

class OAuth2PasswordBearerWithCookie(OAuth2):
    """
    This class is taken directly from FastAPI:
    https://github.com/tiangolo/fastapi/blob/26f725d259c5dbe3654f221e608b14412c6b40da/fastapi/security/oauth2.py#L140-L171
    
    The only change made is that authentication is taken from a cookie
    instead of from the header!
    """
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes}) # type: ignore
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        # IMPORTANT: this is the line that differs from FastAPI. Here we use 
        # `request.cookies.get(settings.COOKIE_NAME)` instead of 
        # `request.headers.get("Authorization")`
        authorization = request.cookies.get(Settings.COOKIE_NAME) 
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = dt.datetime.now() + dt.timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        Settings.SECRET_KEY, 
        algorithm=Settings.ALGORITHM
    )
    return encoded_jwt


def authenticate_user(username: str, plain_password: str) -> Compte | bool:
    user = get_user(username)
    if not user:
        return False
    if not crypto.verify(plain_password, user.mot_de_passe_crypt):
        return False
    return user


def decode_token(token: str | None) -> Compte | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could not validate credentials."
    )
    try:
        token = token.removeprefix("Bearer").strip() # type: ignore
        payload = jwt.decode(token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except JWTError as e:
        print(e)
        raise credentials_exception
    
    user = get_user(username)
    return user


def get_current_user_from_token(token: str = Depends(oauth2_scheme)) -> Compte | None:
    """
    Get the current user from the cookies in a request.

    Use this function when you want to lock down a route so that only 
    authenticated users can see access the route.
    """
    user = decode_token(token)
    return user


def get_current_user_from_cookie(request: Request) -> Compte | None:
    """
    Get the current user from the cookies in a request.
    
    Use this function from inside other routes to get the current user. Good
    for views that should work for both logged in, and not logged in users.
    """
    token = request.cookies.get(Settings.COOKIE_NAME)
    user = decode_token(token)
    return user
