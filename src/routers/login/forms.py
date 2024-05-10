from typing import Optional
from fastapi import Request


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: list = []
        
        
        self.username : Optional[str] = None
        self.password : Optional[str] = None
        

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get("username")
        self.password = form.get("password")
        

    async def is_valid(self):
        if not self.username:
            self.errors.append("Email is required")
        if not self.password or not len(self.password) >= 4:
            self.errors.append("A valid password is required")
        if not self.errors:
            return True
        return False
    






class SignupForm(LoginForm):
    def __init__(self, request: Request):
        super().__init__(request)
        
        self.prenom : Optional[str] = None
        self.nom : Optional[str] = None
        self.telephone : Optional[str] = None
        
        
    async def load_data(self):
        form = await self.request.form()
        self.prenom = form.get("prenom")
        self.nom = form.get("nom")
        self.telephone = form.get("telephone")
        
        self.username = form.get("username")
        self.password = form.get("password")
