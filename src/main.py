from fastapi import Depends, FastAPI, HTTPException, Request, Response, status, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from typing import Annotated, Optional


from datetime import timedelta
from fastapi.security import OAuth2, OAuth2PasswordRequestForm
from fastapi.security.oauth2 import get_authorization_scheme_param, OAuthFlowsModel
from sqlmodel import Session



from api.auth import Settings, User, create_access_token, get_current_user_from_cookie, get_current_user_from_token, authenticate_user





app = FastAPI()
templates = Jinja2Templates(directory="templates")



# class OAuth2PasswordBearerWithCookie(OAuth2):
#     def __init__(
#         self,
#         tokenUrl: str,
#         scheme_name: Optional[str] = None,
#         scopes: Optional[dict[str, str]] = None,
#         description: Optional[str] = None,
#         auto_error: bool = True,
#     ):
#         if not scopes:
#             scopes = {}
#         flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
#         super().__init__(
#             flows=flows,
#             scheme_name=scheme_name,
#             description=description,
#             auto_error=auto_error,
#         )


#     async def __call__(self, request: Request) -> Optional[str]:
#         authorization = request.cookies.get(settings.COOKIE_NAME)
#         scheme, param = get_authorization_scheme_param(authorization)
#         if not authorization or scheme.lower() != "bearer":
#             if self.auto_error:
#                 raise HTTPException(
#                     status_code=status.HTTP_401_UNAUTHORIZED,
#                     detail="Not authenticated",
#                     headers={"WWW-Authenticate": "Bearer"},
#                 )
#             else:
#                 return None
#         return param



# @app.post("/token", response_model=Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(engine, form_data.username, form_data.password)
    
#     print(user)
    
    
#     if user is None:
#         print("Am I reaching this?")
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(data={"sub": user.nom}, expires_delta=access_token_expires)
#     return {"access_token": access_token, "token_type": "bearer"}


# @app.get("/users/me/", response_model=Compte)
# async def read_users_me(current_user: Compte = Depends(get_current_active_user)):
#     return current_user


# # @app.get("/users/me/items") 
# # async def read_users_me_items(current_user: User = Depends(get_current_active_user)):
# #     return [{"id": 1, "owner": current_user}]



# @app.get("/")
# async def root(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})


# @app.get("/signup", response_class=HTMLResponse)
# async def signup(request : Request):
#     return templates.TemplateResponse("signup.html", {"request": request})





# @app.post("/create_account")
# async def create_account(username : Annotated[str, Form()],
#                  email : Annotated[str, Form()],
#                  mot_de_passe : Annotated[str, Form()]):
    
#     hashed_password = get_password_hash(mot_de_passe)
    
#     account = Compte(nom=username, email=email, mot_de_passe_crypt=hashed_password)
    
#     with Session(engine.engine) as session:
#         session.add(account)
#         session.commit()
    
#     return {"username": username, "email": email, "mot_de_passe": mot_de_passe}



# @app.post("/load_account")
# async def load_account(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(engine, form_data.username, form_data.password)
    
#     print(user)
    
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(data={"sub": user.nom}, expires_delta=access_token_expires)
#     return {"access_token": access_token, "token_type": "bearer"}
    
    
    
    
    

@app.post("token")
def login_for_access_token(
    response: Response, 
    form_data: OAuth2PasswordRequestForm = Depends()
) -> dict[str, str]:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    assert isinstance(user, User)
    access_token = create_access_token(data={"username": user.username})
    
    # Set an HttpOnly cookie in the response. `httponly=True` prevents 
    # JavaScript from reading the cookie.
    response.set_cookie(
        key=Settings.COOKIE_NAME, 
        value=f"Bearer {access_token}", 
        httponly=True
    )  
    return {Settings.COOKIE_NAME: access_token, "token_type": "bearer"}


# --------------------------------------------------------------------------
# Home Page
# --------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    try:
        user = get_current_user_from_cookie(request)
    except:
        user = None
    context = {
        "user": user,
        "request": request,
    }
    return templates.TemplateResponse("index.html", context)


# --------------------------------------------------------------------------
# Private Page
# --------------------------------------------------------------------------
# A private page that only logged in users can access.
@app.get("/private", response_class=HTMLResponse)
def private(request: Request, user: User = Depends(get_current_user_from_token)):
    context = {
        "user": user,
        "request": request
    }
    return templates.TemplateResponse("private.html", context)

# --------------------------------------------------------------------------
# Login - GET
# --------------------------------------------------------------------------
@app.get("/auth/login", response_class=HTMLResponse)
def login_get(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("login.html", context)


# --------------------------------------------------------------------------
# Login - POST
# --------------------------------------------------------------------------
class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: list = []
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get("username")
        self.password = form.get("password")

    async def is_valid(self):
        if not self.username or not (self.username.__contains__("@")):
            self.errors.append("Email is required")
        if not self.password or not len(self.password) >= 4:
            self.errors.append("A valid password is required")
        if not self.errors:
            return True
        return False


@app.post("/auth/login", response_class=HTMLResponse)
async def login_post(request: Request):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            response = RedirectResponse("/", status.HTTP_302_FOUND)
            login_for_access_token(response=response, form_data=form) # type: ignore
            form.__dict__.update(msg="Login Successful!")
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password") # type: ignore
            return templates.TemplateResponse("login.html", form.__dict__)
    return templates.TemplateResponse("login.html", form.__dict__)


# --------------------------------------------------------------------------
# Logout
# --------------------------------------------------------------------------
@app.get("/auth/logout", response_class=HTMLResponse)
def logout_get():
    response = RedirectResponse(url="/")
    response.delete_cookie(Settings.COOKIE_NAME)
    return response