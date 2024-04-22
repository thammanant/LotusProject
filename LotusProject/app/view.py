from sqladmin import ModelView, Admin

from app.models import UserInfo, ItemList, MachineKey, BottleTransaction, UserTransactions, Redemption, StaffRedemption, \
    StaffInfo


def generate_admin(app, engine):
    admin = Admin(app, engine)

    # set admin panel name
    admin.title = 'Lotus Admin'

    class UserInfoView(ModelView, model=UserInfo):
        column_list = ('userID', 'accountType', 'totalPoints')
        column_searchable_list = ('userID', 'accountType', 'totalPoints')
        column_filters = ('userID', 'accountType', 'totalPoints')
        column_sortable_list = ('userID', 'accountType', 'totalPoints')
        column_default_sort = ('userID', True)
        column_editable_list = ('userID', 'accountType', 'totalPoints')

    class ItemListView(ModelView, model=ItemList):
        column_list = ('itemID', 'itemName', 'pointsRequired')
        column_searchable_list = ('itemID', 'itemName', 'pointsRequired')
        column_filters = ('itemID', 'itemName', 'pointsRequired')
        column_sortable_list = ('itemID', 'itemName', 'pointsRequired')
        column_default_sort = ('itemID', True)
        column_editable_list = ('itemID', 'itemName', 'pointsRequired')

    class MachineKeyView(ModelView, model=MachineKey):
        column_list = ('machineID', 'key')
        column_searchable_list = ('machineID', 'key')
        column_filters = ('machineID', 'key')
        column_sortable_list = ('machineID', 'key')
        column_default_sort = ('machineID', True)
        column_editable_list = ('machineID', 'key')

    class BottleTransactionView(ModelView, model=BottleTransaction):
        column_list = ('bottleTransactionID', 'points', 'date', 'machineID', 'token')
        column_searchable_list = ('bottleTransactionID', 'points', 'date', 'machineID', 'token')
        column_filters = ('bottleTransactionID', 'points', 'date', 'machineID', 'token')
        column_sortable_list = ('bottleTransactionID', 'points', 'date', 'machineID', 'token')
        column_default_sort = ('bottleTransactionID', True)
        column_editable_list = ('bottleTransactionID', 'points', 'date', 'machineID', 'token')

    class UserTransactionsView(ModelView, model=UserTransactions):
        column_list = ('userID', 'bottleTransactionID')
        column_searchable_list = ('userID', 'bottleTransactionID')
        column_filters = ('userID', 'bottleTransactionID')
        column_sortable_list = ('userID', 'bottleTransactionID')
        column_default_sort = ('userID', True)
        column_editable_list = ('userID', 'bottleTransactionID')

    class RedemptionView(ModelView, model=Redemption):
        column_list = ('redemptionID', 'itemID', 'userID', 'issuedDate', 'redeemedDate', 'status', 'numberOfItems')
        column_searchable_list = (
            'redemptionID', 'itemID', 'userID', 'issuedDate', 'redeemedDate', 'status', 'numberOfItems')
        column_filters = ('redemptionID', 'itemID', 'userID', 'issuedDate', 'redeemedDate', 'status', 'numberOfItems')
        column_sortable_list = (
            'redemptionID', 'itemID', 'userID', 'issuedDate', 'redeemedDate', 'status', 'numberOfItems')
        column_default_sort = ('redemptionID', True)
        column_editable_list = (
            'redemptionID', 'itemID', 'userID', 'issuedDate', 'redeemedDate', 'status', 'numberOfItems')

    class StaffRedemptionView(ModelView, model=StaffRedemption):
        column_list = ('redemptionID', 'staffID')
        column_searchable_list = ('redemptionID', 'staffID')
        column_filters = ('redemptionID', 'staffID')
        column_sortable_list = ('redemptionID', 'staffID')
        column_default_sort = ('redemptionID', True)
        column_editable_list = ('redemptionID', 'staffID')

    class StaffInfoView(ModelView, model=StaffInfo):
        column_list = ('staffID', 'staffName', 'location')
        column_searchable_list = ('staffID', 'staffName', 'location')
        column_filters = ('staffID', 'staffName', 'location')
        column_sortable_list = ('staffID', 'staffName', 'location')
        column_default_sort = ('staffID', True)
        column_editable_list = ('staffID', 'staffName', 'location')

    admin.add_view(UserInfoView)
    admin.add_view(ItemListView)
    admin.add_view(MachineKeyView)
    admin.add_view(BottleTransactionView)
    admin.add_view(UserTransactionsView)
    admin.add_view(RedemptionView)
    admin.add_view(StaffRedemptionView)
    admin.add_view(StaffInfoView)
