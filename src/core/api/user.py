from fastapi import Depends, HTTPException, status

from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

from pydantic import BaseModel
from sqlmodel import Session, select

from api.engine import Engine
from api.models import Compte






SECRET_KEY = "1234" # Horrible secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30






class Token(BaseModel):
    access_token: str
    token_type: str
    
    
    
class TokenData(BaseModel):
    username: str | None = None
    
    

    
    
    
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")





def verify_password(plain_password : str | bytes, hashed_password : str | bytes) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password : str | bytes) -> str:
    return pwd_context.hash(password)


def get_user(engine : Engine, username : str) -> Compte | None:
    with Session(engine.engine) as session:
        user = session.exec(select(Compte)\
                            .where(Compte.nom == username))
        
        return user.first()
    
    
def authenticate_user(engine : Engine, username : str, password : str) -> Compte | None:
    user = get_user(engine, username)
    if not user:
        return None
        
    if not verify_password(password, user.mot_de_passe_crypt):
        return None
        
    return user


def create_access_token(data : dict, expires_delta : timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

    
    
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username : str = payload.get("sub")
        
        
        if username is None:
            raise credentials_exception
            
        token_data = TokenData(username=username)
        
    except JWTError:
        raise credentials_exception
    
    engine = Engine()
    
    assert isinstance(token_data.username, str)
    user = get_user(engine, token_data.username)
    
    print(user, token_data.username)
    
    if user is None:
        raise credentials_exception
    
    
    return user 



async def get_current_active_user(current_user: Compte = Depends(get_current_user)):
    # if current_user.disabled:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is disabled")

    return current_user




