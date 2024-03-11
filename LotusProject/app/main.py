from fastapi import FastAPI
import models
from database import engine
import routers

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(routers.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
