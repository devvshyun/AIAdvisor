from fastapi import FastAPI
from app.services import billing, users
app = FastAPI()
app.include_router(users.router)
app.include_router(billing.router)
