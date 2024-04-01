from fastapi import FastAPI
from app import models
from app.database import engine, SessionLocal, getDB
import app.routers as routers
from app.models import ItemList

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(routers.router)

# pre populate the database
item1 = ItemList(itemID=1, itemName='Egg', pointsRequired=10)
# commit the transaction
with SessionLocal() as db:
    db.add(item1)
    db.commit()

# if __name__ == "__main__":
#     import uvicorn
#
#     uvicorn.run(app, host="0.0.0.0", port=8000)
