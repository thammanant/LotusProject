from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database import Base


class UserInfo(Base):
    __tablename__ = "User Information"

    userID = Column(String, primary_key=True, index=True)
    accountType = Column(String)
    totalPoints = Column(Integer)


class BottleTransaction(Base):
    __tablename__ = "Bottle Transactions"

    bottleTransactionID = Column(Integer, primary_key=True, index=True)
    points = Column(Integer)
    date = Column(DateTime)
    machineID = Column(String, ForeignKey('Machine Key.machineID'))
    token = Column(String)


class MachineKey(Base):
    __tablename__ = "Machine Key"

    machineID = Column(String, primary_key=True, index=True)
    key = Column(String)


class UserTransactions(Base):
    __tablename__ = "User Transactions"

    userID = Column(String, ForeignKey('User Information.userID'), primary_key=True, index=True)
    bottleTransactionID = Column(Integer, ForeignKey('Bottle Transactions.bottleTransactionID'), primary_key=True,
                                 index=True)


class ItemList(Base):
    __tablename__ = "Item List"

    itemID = Column(Integer, primary_key=True, index=True)
    itemName = Column(String)
    pointsRequired = Column(Integer)


class Redemption(Base):
    __tablename__ = "Redemptions"

    redemptionID = Column(String, primary_key=True, index=True)
    itemID = Column(Integer, ForeignKey('Item List.itemID'))
    userID = Column(String, ForeignKey('User Information.userID'))
    issuedDate = Column(DateTime)
    redeemedDate = Column(DateTime)
    status = Column(String)
    numberOfItems = Column(Integer)


class StaffRedemption(Base):
    __tablename__ = "Staff Redemptions"

    redemptionID = Column(String, ForeignKey('Redemptions.redemptionID'), primary_key=True, index=True)
    staffID = Column(Integer, ForeignKey('Staff Information.staffID'), primary_key=True, index=True)


class StaffInfo(Base):
    __tablename__ = "Staff Information"

    staffID = Column(Integer, primary_key=True, index=True)
    staffName = Column(String)
    location = Column(String)
