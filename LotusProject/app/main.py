from fastapi import FastAPI
from app import models
from app.database import engine, SessionLocal
import app.routers as routers
from app.models import ItemList, MachineKey
from app.view import generate_admin

app = FastAPI()

# remove all tables
models.Base.metadata.drop_all(engine)
# create all tables
models.Base.metadata.create_all(engine)

app.include_router(routers.router)

# check if the database is empty
with SessionLocal() as db:
    item = db.query(ItemList).first()
    # if empty, add items
    if not item:
        # pre populate the database
        item1 = ItemList(itemID=1, itemName='ไข่ไก่', pointsRequired=10)

        db.add(item1)
        db.commit()

    machine = db.query(MachineKey).first()
    # if empty, add machine key
    if not machine:
        # pre populate the database
        machine1 = MachineKey(machineID="1", key='c435d980d70d')

        db.add(machine1)
        db.commit()

# create admin
generate_admin(app, engine)

# if __name__ == '__main__':
#     import uvicorn
#
#     uvicorn.run(app, host="0.0.0.0", port=8000)
