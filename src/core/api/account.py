

from fastapi import HTTPException
from .models import Proprietaire
from .auth import authenticate_user, create_access_token


class Account:
    
    
    @classmethod
    def login(cls, email : str, password : str) -> tuple["Proprietaire", str]:
        user = authenticate_user(email, password)
        
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
            
        access_token = create_access_token(data={"username": user.email})
        
        return user, access_token
    
    
    @classmethod
    def signup(cls, user : Proprietaire):
        pass