from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base


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
    __tablename__ = "User Transactions"

    userID = Column(String, ForeignKey('User_Information.userID'), primary_key=True, index=True)
    transactionID = Column(Integer, ForeignKey('Transactions.transactionID'), primary_key=True, index=True)
