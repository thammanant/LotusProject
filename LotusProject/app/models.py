from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base


class User_bottles(Base):
    __tablename__ = "user_bottles"

    userID = Column(Integer, primary_key=True, index=True)
    bottleNumber = Column(String, index=True)