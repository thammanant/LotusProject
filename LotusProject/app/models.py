from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database import Base


class UserInfo(Base):
    __tablename__ = "User_Information"

    userID = Column(String, primary_key=True, index=True)
    accountType = Column(String)
    totalPoints = Column(Integer)


class Transactions(Base):
    __tablename__ = "Transactions"

    transactionID = Column(Integer, primary_key=True, index=True)
    points = Column(Integer)
    date = Column(DateTime)
    location = Column(String)


class UserTransactions(Base):
    __tablename__ = "User_Transactions"

    userID = Column(String, ForeignKey('User_Information.userID'), primary_key=True, index=True)
    transactionID = Column(Integer, ForeignKey('Transactions.transactionID'), primary_key=True, index=True)


class ItemList(Base):
    __tablename__ = "Item_List"

    itemID = Column(Integer, primary_key=True, index=True)
    itemName = Column(String)
    pointsRequired = Column(Integer)


class Redemption(Base):
    __tablename__ = "Redemption"

    redemptionID = Column(Integer, primary_key=True, index=True)
    userID = Column(String, ForeignKey('User_Information.userID'))
    itemID = Column(Integer, ForeignKey('Item_List.itemID'))
    date = Column(DateTime)

