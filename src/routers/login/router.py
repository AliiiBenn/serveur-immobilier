from fastapi import APIRouter


from fastapi import Depends, HTTPException, Request, Response, status
from fastapi.datastructures import FormData
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates



from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from passlib.handlers.sha2_crypt import sha512_crypt as crypto



from core.api.models import Proprietaire
from core.api.auth import Settings, create_access_token, get_current_user_from_cookie, get_current_user_from_token, authenticate_user

from core.api.engine import Engine
from core.api.account import Account

from .forms import LoginForm, SignupForm


router = APIRouter()
engine = Engine()

templates = Jinja2Templates(directory="../templates")


    

@router.post("token")
def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
    user, access_token = Account.login(form_data.username, form_data.password)
    
    # Set an HttpOnly cookie in the response. `httponly=True` prevents 
    # JavaScript from reading the cookie.
    response.set_cookie(
        key=Settings.COOKIE_NAME, 
        value=f"Bearer {access_token}", 
        httponly=True
    ) 
    return {Settings.COOKIE_NAME: access_token, "token_type": "bearer"}






@router.get("/private", response_class=HTMLResponse)
def private(request: Request, user: Proprietaire = Depends(get_current_user_from_token)):
    context = {
        "user": user,
        "request": request
    }
    return templates.TemplateResponse("private.html", context)

# --------------------------------------------------------------------------
# Login - GET
# --------------------------------------------------------------------------
@router.get("/auth/login", response_class=HTMLResponse)
def login_get(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("login.html", context)


# --------------------------------------------------------------------------
# Login - POST
# --------------------------------------------------------------------------

    
    


@router.post("/auth/login", response_class=HTMLResponse)
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
@router.get("/auth/logout", response_class=HTMLResponse)
def logout_get():
    response = RedirectResponse(url="/")
    response.delete_cookie(Settings.COOKIE_NAME)
    return response




@router.get("/auth/signup", response_class=HTMLResponse)
def signup_get(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("signup.html", context)






@router.post("/auth/signup", response_class=HTMLResponse)
async def signup_post(request: Request):
    form = SignupForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            hashed_password = crypto.hash(form.password)
            
            with Session(engine.engine) as session:
                compte = Proprietaire(
                    prenom=form.prenom,
                    nom=form.nom,
                    telephone=form.telephone,
                    email=form.username,
                    mot_de_passe_hash=crypto.hash(form.password)
                )
                
                session.add(compte)
                session.commit()
            
            
            response = RedirectResponse("/", status.HTTP_302_FOUND)
            login_for_access_token(response=response, form_data=form) # type: ignore
            form.__dict__.update(msg="Login Successful!")
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password") # type: ignore
            return templates.TemplateResponse("signup.html", form.__dict__)
    return templates.TemplateResponse("signup.html", form.__dict__)







