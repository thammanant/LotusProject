from fastapi import FastAPI
from app import models
from app.database import engine
import app.routers as routers

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(routers.router)
