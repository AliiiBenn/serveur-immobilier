from fastapi import FastAPI

import routers.login as login



app = FastAPI()

app.include_router(login.router)

