from fastapi import FastAPI
from app import models
from app.database import engine, SessionLocal
import app.routers as routers
from app.models import UserInfo, ItemList, MachineKey, BottleTransaction, UserTransactions, Redemption, StaffRedemption, \
    StaffInfo
from sqladmin import Admin, ModelView

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
        machine1 = MachineKey(machineID="1", key='1234')

        db.add(machine1)
        db.commit()

admin = Admin(app, engine)


class UserInfo(ModelView, model=UserInfo):
    column_list = ('userID', 'accountType', 'totalPoints')
    column_searchable_list = ('userID', 'accountType', 'totalPoints')
    column_filters = ('userID', 'accountType', 'totalPoints')
    column_sortable_list = ('userID', 'accountType', 'totalPoints')
    column_default_sort = ('userID', True)
    column_editable_list = ('userID', 'accountType', 'totalPoints')


class ItemList(ModelView, model=ItemList):
    column_list = ('itemID', 'itemName', 'pointsRequired')
    column_searchable_list = ('itemID', 'itemName', 'pointsRequired')
    column_filters = ('itemID', 'itemName', 'pointsRequired')
    column_sortable_list = ('itemID', 'itemName', 'pointsRequired')
    column_default_sort = ('itemID', True)
    column_editable_list = ('itemID', 'itemName', 'pointsRequired')


class MachineKey(ModelView, model=MachineKey):
    column_list = ('machineID', 'key')
    column_searchable_list = ('machineID', 'key')
    column_filters = ('machineID', 'key')
    column_sortable_list = ('machineID', 'key')
    column_default_sort = ('machineID', True)
    column_editable_list = ('machineID', 'key')


class BottleTransaction(ModelView, model=BottleTransaction):
    column_list = ('bottleTransactionID', 'points', 'date', 'machineID', 'token')
    column_searchable_list = ('bottleTransactionID', 'points', 'date', 'machineID', 'token')
    column_filters = ('bottleTransactionID', 'points', 'date', 'machineID', 'token')
    column_sortable_list = ('bottleTransactionID', 'points', 'date', 'machineID', 'token')
    column_default_sort = ('bottleTransactionID', True)
    column_editable_list = ('bottleTransactionID', 'points', 'date', 'machineID', 'token')


class UserTransactions(ModelView, model=UserTransactions):
    column_list = ('userID', 'bottleTransactionID')
    column_searchable_list = ('userID', 'bottleTransactionID')
    column_filters = ('userID', 'bottleTransactionID')
    column_sortable_list = ('userID', 'bottleTransactionID')
    column_default_sort = ('userID', True)
    column_editable_list = ('userID', 'bottleTransactionID')


class Redemption(ModelView, model=Redemption):
    column_list = ('redemptionID', 'itemID', 'userID', 'issuedDate', 'redeemedDate', 'status', 'numberOfItems')
    column_searchable_list = (
        'redemptionID', 'itemID', 'userID', 'issuedDate', 'redeemedDate', 'status', 'numberOfItems')
    column_filters = ('redemptionID', 'itemID', 'userID', 'issuedDate', 'redeemedDate', 'status', 'numberOfItems')
    column_sortable_list = ('redemptionID', 'itemID', 'userID', 'issuedDate', 'redeemedDate', 'status', 'numberOfItems')
    column_default_sort = ('redemptionID', True)
    column_editable_list = ('redemptionID', 'itemID', 'userID', 'issuedDate', 'redeemedDate', 'status', 'numberOfItems')


class StaffRedemption(ModelView, model=StaffRedemption):
    column_list = ('redemptionID', 'staffID')
    column_searchable_list = ('redemptionID', 'staffID')
    column_filters = ('redemptionID', 'staffID')
    column_sortable_list = ('redemptionID', 'staffID')
    column_default_sort = ('redemptionID', True)
    column_editable_list = ('redemptionID', 'staffID')


class StaffInfo(ModelView, model=StaffInfo):
    column_list = ('staffID', 'staffName', 'location')
    column_searchable_list = ('staffID', 'staffName', 'location')
    column_filters = ('staffID', 'staffName', 'location')
    column_sortable_list = ('staffID', 'staffName', 'location')
    column_default_sort = ('staffID', True)
    column_editable_list = ('staffID', 'staffName', 'location')


admin.add_view(UserInfo)
admin.add_view(ItemList)
admin.add_view(MachineKey)
admin.add_view(BottleTransaction)
admin.add_view(UserTransactions)
admin.add_view(Redemption)
admin.add_view(StaffRedemption)
admin.add_view(StaffInfo)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)