from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.admin.auth import authentication_backend
from app.database import engine
from app.users.router import router as router_user

from sqladmin import Admin

app = FastAPI()
app.include_router(router_user)
app.mount('/media', StaticFiles(directory='media'), name='media')
admin = Admin(app, engine=engine, authentication_backend=authentication_backend)
origins = [
    "http:localhost:5173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

