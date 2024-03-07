from fastapi import FastAPI
import models
from database import engine
import routers

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(routers.router)

